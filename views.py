from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from .models import Todo, Message,Good

from .forms import MessageForm,TodoForm



class TodoList(ListView):
    model = Todo
    context_object_name = "tasks"


class TodoDetail(DetailView):
    model = Todo
    context_object_name = "task"

class TodoCreate(CreateView):
    model = Todo
    form_class=TodoForm
    success_url = reverse_lazy("list")
    def form_valid(self,form):
        msg=Message()
        msg.owner=self.request.user
        msg.content=self.request.POST["description"]
        msg.save()
        return super().form_valid(form)

class TodoUpdate(UpdateView):
    model = Todo
    # fields = "__all__"
    form_class=TodoForm
    success_url = reverse_lazy("list")

class TodoDelete(DeleteView):
    model = Todo
    context_object_name = "task"
    success_url = reverse_lazy("list")


def todo_list(request):
    tasks = Todo.objects.all()
    selected_tasks = request.session.get('selected_tasks', [])
    
    if request.method == 'POST':
        selected_tasks = request.POST.getlist('selected_tasks')
        request.session['selected_tasks'] = selected_tasks
        return redirect('todo_list')
    
    return render(request, 'todo_list.html', {'tasks': tasks, 'selected_tasks': selected_tasks})



# indexのビュー関数
@login_required(login_url='/admin/login/')
def index(request, page=1):
    print(request.session.keys())
    print(request.session["_auth_user_id"])
    max = 10 #ページ当たりの表示数
    form = MessageForm() #PostFormから変更
    msgs = Message.objects.all()
    # ページネーションで指定ページを取得
    paginate = Paginator(msgs, max)
    page_items = paginate.get_page(page)

    params = {
        'login_user':request.user,
        'form': form,
        'contents':page_items,
    }
    return render(request, 'todo_sns/index.html', params)

# goodsのビュー関数
@login_required(login_url='/admin/login/')
def goods(request):
    goods = Good.objects.filter(owner=request.user)
    params = {
        'login_user':request.user,
        'contents':goods,
    }
    return render(request, 'todo_sns/good.html', params)

# メッセージのポスト処理
@login_required(login_url='/admin/login/')
def post(request):
    # POST送信の処理
    if request.method == 'POST':
        form = MessageForm(request.POST) #PostFormから変更
        if form.is_valid():
        #ModelFormの保存方法に変更
            post = form.save(commit=False) #保存前処理
            post.owner = request.user  # ログインしているユーザーを取得
            post.save()
            return redirect(to='/todo_sns/')
    else:
        messages = Message.objects.filter(owner=request.user)
        params = {
            'login_user':request.user,
            'contents':messages,
        }
        return render(request, 'todo_sns/post.html', params)

# goodボタンの処理
@login_required(login_url='/admin/login/')
def good(request, good_id):
    # goodするMessageを取得
    good_msg = Message.objects.get(id=good_id)
    print(good_msg)
    # 自分がメッセージにGoodした数を調べる
    is_good = Good.objects.filter(owner=request.user) \
        .filter(message=good_msg).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        good_record=Good.objects.filter(owner=request.user) \
        .filter(message=good_msg)
        good_record.delete()
        good_msg.good_count -=1
        good_msg.save()
        messages.success(request, 'goodを解除しました。')
        return redirect(to='/todo_sns')
    
    # Messageのgood_countを１増やす
    good_msg.good_count += 1
    good_msg.save()
    # Goodを作成し、設定して保存
    good = Good()
    good.owner = request.user
    good.message = good_msg
    good.save()
    # メッセージを設定
    messages.success(request, 'メッセージにGoodしました！')
    return redirect(to='/todo_sns')

@login_required(login_url='/admin/login/')
def edit(request, message_id):
    obj=Message.objects.get(id=message_id)
    if request.method == "POST":
        message_record =MessageForm(request.POST,instance=obj)
        message_record.save()
        return redirect(to="/todo_sns")
    params = {
        'login_user':request.user,
        'form':MessageForm(instance=obj),
        "id":message_id
    }
    return render(request,"todo_sns/edit.html",params)

@login_required(login_url='/admin/login/')
def delete(request,message_id):
    msg=Message.objects.get(id=message_id)
    msg.delete()
    return redirect(to="/todo_sns/post")


def find(request,num):
        messages = Message.objects.filter(owner=num)
        params = {
            'login_user':request.user,
            'contents':messages
        }
        return render(request, 'todo_sns/find.html', params)
