from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.base import TemplateView

from .models import Area, Project, Column, Item

#atuthentication stuff
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required

#forms
from .forms import NewItemForm

"""
There is a main todo list which draws from all areas, projects and items, arranged by priority
There are area todo lists which draws from all projects and items in the area, arranged by priority
There are project todo lists which draws from all items in the project, arranged by priority
When actions are completed, in one list, they are completed in all lists
"""

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("kanban_app:login")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="kanban_app/user_auth/register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("kanban_app:areas")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="kanban_app/user_auth/login.html", context={"login_form":form})

def logout_request(request):
    if request.method == 'post':
        a = request.POST.get('')
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("kanban_app:login")

class PriorityView(generic.ListView):
    login_required = True

    def shift_priority(self, request, Model, obj_id):
        obj=Model.objects.filter(id=obj_id).get()
        current_priority = obj.priority
        if request.POST['submit']=='Higher':
            if obj.priority!=1:
                obj.priority= current_priority-1
                obj.save()
        if request.POST['submit']=='Lower':
            if obj.priority!=5:
                obj.priority= current_priority+1
                obj.save()

class Landing(TemplateView):
    """A place for non authenticated users to go...
    """
    template_name = 'kanban_app/landing.html'

class AreaList(PriorityView):#all areas owned by user
    """Shows list of areas (ordered by priority) and associated projects
    On this page users can:
    (post)
    -create a new area
    -reprioritise areas
    (links)
    -area pages
    -project pages
    -create area project
    -delete area
    """
    model = Area

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by('priority')

    def post(self, request, *args, **kwargs):
        if request.POST['submit']=='Create new area':
            user=request.user
            num_areas=Area.objects.filter(user=user).count() + 1
            priority=num_areas if num_areas<5 else 5
            area=Area(user=user, name=request.POST['new'], priority=priority)
            area.save()
            return redirect('kanban_app:areas')
        
        self.shift_priority(request, Area, request.POST['priority'])
        return redirect('kanban_app:areas')

class AreaDelete(generic.TemplateView):
    """Shows an area and associated projects to be deleted
    (post)
    -confirm delete area
    (links)
    -area list
    -logout
    """
    login_required = True
    def get(self, request, *args, **kwargs):
        area_name = kwargs['area']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        context={'area':area}
        return render(request, 'kanban_app/area_delete.html', context)

    def post(self, request, *args, **kwargs):
        area_name = kwargs['area']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        area.delete()
        return redirect('kanban_app:areas')

class AreaView(PriorityView):
    """Shows a single area and associated projects
    (post)
    -project priority up
    -project priority down
    (link)
    -create new blank project
    -logout
    -individual project
    -delete individual project
    -create new project using project as template
    """
    def get(self, request, *args, **kwargs):
        user=request.user
        area_name=kwargs['area']
        area=Area.objects.filter(user=user,name=area_name).get()
        bad_projects = Project.objects.filter(user=request.user, template=True).all()
        bad_projects.delete()
        return render(request,'kanban_app/area_view.html',{'area':area})

    def post(self, request, *args, **kwargs):
        area_name=kwargs['area']
        self.shift_priority(request, Project, request.POST['priority'])
        return redirect('kanban_app:area',area_name)
        
class ProjectCreate(generic.TemplateView):
    login_required = True

    def post(self, request, *args, **kwargs):
        user=request.user
        area_name = kwargs['area']
        project_name = kwargs['project']
        project=Project.objects.filter(user=user, name=project_name).get()
        area=Area.objects.filter(user=user, name=area_name).get()
        refresh = redirect('kanban_app:create_project',area_name,project_name)#can be used wherever project name does not change
        
        if request.POST['submit']=='Reset':
            project_name='new'
            return redirect('kanban_app:create_project',area_name,project_name)

        if request.POST['submit']=='Change name':
            new_project_name = request.POST['project_name']
            project.name=new_project_name
            project.save()
            project_name=new_project_name
            return redirect('kanban_app:create_project',area_name,project_name)

        if request.POST['submit']=='Quit and forget':
            area.projects.remove(project)
            project.delete()
            return redirect('kanban_app:area',area_name)

        if request.POST['submit']=='Save and use':
            project.template=False
            project.save()
            return redirect('kanban_app:project',area_name,project_name)

        columns=project.columns.all().order_by('position')
        if request.POST['submit']=='Create column':
            new_position = (len(columns)*2)-1#automatically place new columns second to last
            #print(new_position)
            column=Column(name=request.POST['column_name'], position=new_position)
            column.save()
            project.columns.add(column.id)
            return refresh
        
        column_id = request.POST['column_id']

        column=Column.objects.filter(id=column_id).get()#current column
        if request.POST['submit']=='X':
            #print(project.columns.all())
            project.columns.remove(column.id)
            #print(project.columns.all())
            column = Column.objects.filter(id=column_id).get()
            column.delete()
            return refresh
        
        #these require columns to be properly ordered, so...
        
        for i, col in enumerate(columns):
            col.position=(i+1)*2#allows movement by one either side without juggling other columns
        
        position=column.position#position of the new column to be added

        if request.POST['submit']=='>>':
            #2, 4, 6, 8 with 4 to move forward
            if column.position != len(columns)*2:
                column.position=position+3#requires position + 3
                column.save()
            return refresh
        elif request.POST['submit']=='<<':
            #2, 4, 6, 8 with 4 to move backward
            if column.position!=2:
                column.position=position-3#requires position - 3
                column.save()
            return refresh
        
    def get(self, request, *args, **kwargs):
        user=request.user
        area_name = kwargs['area']
        project_name = kwargs['project']
        area=Area.objects.filter(user=user, name=area_name).get()

        def auto_columns(project):
            for count,name in enumerate(('Backlog','Done')):
                column=Column(name=name, position=count*2)
                column.save()
                project.columns.add(column.id)
            new_project.save()
                
        if project_name == 'new':
            project_name='To do'
            new_project = Project(user= user, name=project_name)
            new_project.save()
            area.projects.add(new_project.id)
            auto_columns(new_project)
            return redirect('kanban_app:create_project',area_name,project_name)
        
        try:
            project=Project.objects.filter(user=user, name=project_name).get()
            print('MultipleObjectsReturned Error, so trying this instead...')
        except:
            print('Here goes...')
            projects=Project.objects.filter(user=user, name=project_name).all()
            #print(projects)
            for project in projects[1:]:
                project.delete()
            project=projects[0]     
        
        if project.template==False:
            project=Project.objects.filter(user=user, name=project_name).get()
            new_project_name = project_name+' template'
            new_project = Project(user=user, name=new_project_name)
            new_project.save()
            area.projects.add(new_project.id)
            auto_columns(new_project)
            for col in project.columns.all():
                new_column = Column(name = col.name, position=col.position)
                new_column.save()
                new_project.columns.add(new_column)

            project_name = new_project_name
            return redirect('kanban_app:create_project',area_name,project_name)

        project=Project.objects.filter(user=user, name=project_name).get()
        columns = project.columns.all().order_by('position')

        for i, col in enumerate(columns):
            col.position=(i+1)*2#allows movement by one either side without juggling other columns
            col.save()
            #print(col.name, col.position)
        new_position = len(columns)+1
        context={
            'project':project,
            'columns':columns,
            'new_position':new_position,
        }
        return render(request, 'kanban_app/project_create.html', context)

class ProjectDelete(generic.ListView):
    """Shows a project and associated columns to be deleted
    (post)
    -confirm delete column
    (links)
    -area list
    -logout
    """
    login_required = True
    def get(self, request, *args, **kwargs):
        area_name = kwargs['area']
        project_name = kwargs['project']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        project=Project.objects.filter(user=request.user,name=project_name).get() 
        context={'area':area, 'project':project}
        return render(request, 'kanban_app/project_delete.html', context)

    def post(self, request, *args, **kwargs):
        area_name = kwargs['area']
        project_name = kwargs['project']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        project=Project.objects.filter(user=request.user,name=project_name).get() 
        area.projects.remove(project.id)
        project.delete()
        return redirect('kanban_app:area',area_name)

class AreaDelete(generic.TemplateView):
    """Shows an area and associated projects to be deleted
    (post)
    -confirm delete area
    (links)
    -area list
    -logout
    """
    login_required = True
    def get(self, request, *args, **kwargs):
        area_name = kwargs['area']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        return render(request, 'kanban_app/project_delete.html', {'area':area})

    def post(self, request, *args, **kwargs):
        area_name = kwargs['area']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        area.delete()
        return redirect('kanban_app:areas')

class ProjectView(generic.TemplateView):

    login_required = True
    def get(self, request, *args, **kwargs):
        area_name = kwargs['area']
        project_name = kwargs['project']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        project=Project.objects.filter(user=request.user,name=project_name).get()
        columns = project.columns.all().order_by('position')
        context = {
            'area':area,
            'project':project,#first we got this up above...
            'columns':columns,
            'NewItemForm':NewItemForm(user=request.user)
        }
        return render(request, 'kanban_app/project.html', context)

    def post(self, request, *args, **kwargs):
        area_name = kwargs['area']
        project_name = kwargs['project']
        area=Area.objects.filter(user=request.user, name=area_name).get()
        project=Project.objects.filter(user=request.user,name=project_name).get() 
        refresh = redirect('kanban_app:project',area_name,project_name)

        def save_comments(request):
            item.comment=request.POST['comment']            
            item.save()
            return refresh


        if request.POST['submit']=='New item':
            #form = NewItemForm(request.POST)
            
            item_name = request.POST['item_name']
            column = Column.objects.filter(position=2, columns__in=[project]).get()#column positions go up in 2s...see create project
            num=column.items.count() + 1
            priority=num if num<5 else 5
            item = Item(user= request.user, name=item_name, priority=priority)
            item.save()
            column.items.add(item.id)#add to new column    
            return refresh
            
        item_id = int(request.POST['item_id'])#needed for all next actions
        item = Item.objects.filter(id = item_id).get()#item
        
        if request.POST['submit']=='Delete':
            item.delete()
            return refresh

        column_id = int(request.POST['column_id'])
        column = Column.objects.filter(id = column_id).get()#column
        column_position = int(request.POST['column_position'])
        
        def move_item(border, change, column, item, column_position):
            '''used below
            '''
            if column_position !=border:#if column not last one in list, or first
                column.items.remove(item.id)#remove from current column
                new_position = column_position + change#get new column position (+ or - 1)
                new_column = Column.objects.filter(position=new_position, columns__in=[project]).get()#get new column
                new_column.items.add(item.id)#add to new column

        if request.POST['submit']=='<<':
            save_comments(request)
            move_item(2, -2, column, item, column_position)
            return refresh
        elif request.POST['submit']=='>>':
            save_comments(request)
            move_item(len(project.columns.all())*2, 2, column, item, column_position)               
            return refresh

        def change_priority(limit, change, item):
            #print(item)
            if item.priority != limit:
                item.priority += change
                item.save()
        
        if request.POST['submit']=='Higher':
            #print('higher')
            save_comments(request)
            change_priority(1, -1, item)            
            return refresh
        elif request.POST['submit']=='Lower':
            #print('lower')
            save_comments(request)
            change_priority(5, +1, item)
            return refresh

        if request.POST['submit']=='Save':
            return save_comments(request)


        if request.POST['submit']=='Mark as blocked':
            save_comments(request)
            item.blocked=True
            item.save()    
            return refresh
        if request.POST['submit']=='Mark as clear':
            save_comments(request)
            item.blocked=False
            item.save()
            return refresh
        