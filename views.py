from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic.base import TemplateView

from .models import Project, Column, Item

#atuthentication stuff
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth.decorators import login_required

#forms
from .forms import NewItemForm


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
                return redirect("kanban_app:home")
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

class Landing(TemplateView):
    template_name = 'kanban_app/landing.html'

class ProjectList(generic.ListView):
    #all posts belonging to user
    model = Project

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, template=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bad_projects = self.model.objects.filter(user=self.request.user, template=True).all()
        bad_projects.delete()
        return context

def delete(request):
    if request.user.is_authenticated:
        context = {
            'projects':Project.objects.filter(user=request.user, template=False)
        }
        return render(request, 'kanban_app/delete_project.html', context)
        
def confirm_delete(request, project_name):
    if request.user.is_authenticated:
        user_id = request.user.id#used in both conditions
        project = Project.objects.filter(user = user_id, name = project_name).get()
        if request.method == 'POST':
            if request.POST['submit']=='Confirm delete':
                project.delete()
                return redirect("kanban_app:home")
        else:
            columns = project.columns.all().order_by('position')
            context = {
                'project':project,#first we got this up above...
                'columns':columns,
            }
            return render(request, 'kanban_app/confirm_delete.html', context)


def project_view(request, project_name):
    if request.user.is_authenticated:
        user_id = request.user.id#used in both conditions
        project = Project.objects.filter(user = user_id, name = project_name).get()
        print(project_name)
        print(project)
        if request.method == 'POST':
            refresh = redirect('kanban_app:project_view', project_name=project_name)

            if request.POST['submit']=='New item':
                #form = NewItemForm(request.POST)
                
                item_name = request.POST['item_name']
                item = Item(user= request.user, name=item_name)
                item.save()
                column = Column.objects.filter(position=2, columns__in=[project]).get()#column positions go up in 2s...see create project
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
                """used below
                """
                if column_position !=border:#if column not last one in list, or first
                    column.items.remove(item.id)#remove from current column
                    new_position = column_position + change#get new column position (+ or - 1)
                    new_column = Column.objects.filter(position=new_position, columns__in=[project]).get()#get new column
                    new_column.items.add(item.id)#add to new column

            if request.POST['submit']=='<<':
                move_item(2, -2, column, item, column_position)
                return refresh
            elif request.POST['submit']=='>>':
                move_item(len(project.columns.all())*2, 2, column, item, column_position)               
                return refresh

            def change_priority(limit, change, item):
                print(item)
                if item.priority != limit:
                    item.priority += change
                    item.save()
            
            if request.POST['submit']=='Higher':
                print('higher')
                change_priority(1, -1, item)
                
                return refresh
            elif request.POST['submit']=='Lower':
                print('lower')
                change_priority(5, +1, item)
                return refresh

        else:
            columns = project.columns.all().order_by('position')
            context = {
                'project':project,#first we got this up above...
                'columns':columns,
                'NewItemForm':NewItemForm(user=request.user)
            }
            return render(request, 'kanban_app/project.html', context)
    else:
        return redirect('kanban_app:login')

def create_project(request, project_name):
    if request.user.is_authenticated:
        user = request.user
        refresh = redirect('kanban_app:create_project', project_name)#can be used wherever project name does not change
        print(project_name)
        
        if project_name == 'new':
            project_name='Fresh new project'
            new_project = Project(user= user, name=project_name)
            new_project.save()
            return redirect('kanban_app:create_project', project_name)

        elif request.method == 'POST':
            if request.POST['submit']=='Reset':
                project_name='new'
                return redirect('kanban_app:create_project', project_name)

            project=Project.objects.filter(user=user, name=project_name).get()
            
            if request.POST['submit']=='Change name':
                new_project_name = request.POST['project_name']
                project.name=new_project_name
                project.save()
                project_name=new_project_name
                return redirect('kanban_app:create_project', project_name)

            if request.POST['submit']=='Quit and forget':
                project.delete()
                return redirect('kanban_app:home')

            if request.POST['submit']=='Save and use':
                project.template=False
                project.save()
                return redirect('kanban_app:project_view', project_name)

            columns=project.columns.all().order_by('position')
            if request.POST['submit']=='Create column':
                new_position = (len(columns)+1)*2
                print(new_position)
                column=Column(name=request.POST['column_name'], position=new_position)
                column.save()
                project.columns.add(column.id)
                return refresh
            
            column_id = request.POST['column_id']

            column=Column.objects.filter(id=column_id).get()#current column
            if request.POST['submit']=='Delete':
                print(project.columns.all())
                project.columns.remove(column.id)
                print(project.columns.all())
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
            elif request.POST['submit']=='<<':
                #2, 4, 6, 8 with 4 to move backward
                if column.position!=2:
                    column.position=position-3#requires position - 3
                    column.save()

            return refresh
        
        else:
            try:
                project=Project.objects.filter(user= user, name=project_name).get()
                print('MultipleObjectsReturned Error, so trying this instead...')
            except:
                print('Here goes...')
                projects=Project.objects.filter(user= user, name=project_name).all()
                print(projects)
                for project in projects[1:]:
                    project.delete()
                project = projects[0]     
            
            if project.template==False:
                project=Project.objects.filter(user= user, name=project_name).get()
                new_project_name = project_name+' template'
                new_project = Project(user=user, name=new_project_name)
                new_project.save()
                for col in project.columns.all():
                    new_column = Column(name = col.name, position=col.position)
                    new_column.save()
                    new_project.columns.add(new_column)

                project_name = new_project_name
                return redirect('kanban_app:create_project', project_name)

            project = Project.objects.filter(user= user, name=project_name).get()
            columns = project.columns.all().order_by('position')
            for i, col in enumerate(columns):
                col.position=(i+1)*2#allows movement by one either side without juggling other columns
                col.save()
                print(col.name, col.position)
            new_position = len(columns)+1
            context={
                'project':project,
                'columns':columns,
                'new_position':new_position,
            }
            return render(request, 'kanban_app/create_project.html', context)
    else:
        return redirect('kanban_app:login')
