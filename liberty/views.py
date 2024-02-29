from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
import datetime
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View

from .forms import LoginForm, UserRegistrationForm, ItemCreateForm, ItemUpdateForm
from .models import User, Category, Item, ItemLike


class HomePageView(View):
    template_name = 'index.html'
    def get(self,request):
        categories = Category.objects.all()
        items = Item.objects.all()
        item01=Item.objects.filter(category=Category.objects.get(id=1)).first()
        item2=Item.objects.filter(category=Category.objects.get(id=2)).first()
        item3=Item.objects.filter(category=Category.objects.get(id=3)).first()
        item4=Item.objects.filter(category=Category.objects.get(id=4)).first()
        item5=Item.objects.filter(category=Category.objects.get(id=5)).first()
        item6=Item.objects.filter(category=Category.objects.get(id=6)).first()
        return render(request, self.template_name, {'categories': categories
                                                    ,'items': items,'item01':item01,'item2':item2,'item3':item3,
                                                    'item4':item4,'item5':item5,'item6':item6})



class CategoryDetailView(View):
    def get(self, request, pk):
        category = Category.objects.get(pk=pk)
        items = sorted(Item.objects.filter(category=category), key=lambda o: o.like_count, reverse=True)
        context = {
            "category": category,
            "items": items,
       }
        return render(request, "category_list.html", context=context)

class ItemsListView(View):

    def get(self, request):
        items = Item.objects.all()
        context = {
            "items": items,
        }
        return render(request, "items_list.html", context=context)

class ExploreView(View):
    model = Item
    def get(self, request):
        items = Item.objects.all()
        size = request.GET.get("size", 4)
        page = request.GET.get("page", 1)
        paginator = Paginator(items, size)
        page_obj = paginator.page(page)
        return render(request, "explore.html", context={'items': items,"page_obj": page_obj, "num_pages": paginator.num_pages})

class SearchExploreView(View):
    def get(self, request):
        q = request.GET.get('q', None)
        if q:
            items = Item.objects.filter(Q(title__icontains=q) | Q(description__icontains=q))
        else:
            items = None

        context = {
            'param': q,
            'items': items
        }
        return render(request, 'search_explore.html', context=context)


def post_detail(request, pk):
    item = Item.objects.get(pk=pk)
    b = datetime.datetime.now()
    return render(request, "details.html", {"item": item, "b": b})


def register_view(request):
    form = UserRegistrationForm()
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully registered")
            return redirect('liberty:login-page')
        else:
            return render(request, "register.html", {"form": form})
    else:
        return render(request, "register.html", {"form": form})


class UserLoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print(request.COOKIES)
                messages.success(request, "user successfully logged in")
                return redirect("liberty:index")
            else:
                messages.error(request, "Username or password wrong")
                return redirect("liberty:login-page")

        else:
            return render(request, "login.html", {"form": form})


class UserLogoutView(View):
    def get(self, request):
        return render(request, "logout.html")

    def post(self, request):
        logout(request)
        messages.info(request, "User successfully loged out")
        return redirect("liberty:login-page")

def user_profile(request, username):
    items = Item.objects.filter(author__username=username)
    user = get_object_or_404(User, username=username)
    first_name = user.first_name
    last_name = user.last_name
    return render(request, "author.html", {"items": items,
                                                    "user": user,
                                                    "first_name": first_name,
                                                    "last_name": last_name})


@login_required()
def post_create(request):
    if request.method == "POST":
        form = ItemCreateForm(request.POST)
        if form.is_valid():
            item = Item(title=form.cleaned_data["title"], description=form.cleaned_data["description"],
                        category=form.cleaned_data["category"], ends_in=form.cleaned_data["ends_in"],
                        price=form.cleaned_data["price"],owner_name=form.cleaned_data["owner_name"],
                        owner_username=form.cleaned_data["owner_username"], image=form.cleaned_data["image"],
                        author=request.user)
            # item.author = request.user
            item.save()
            messages.success(request, "item successfully created")
            return redirect(reverse('liberty:author', kwargs={"username": request.user.username}))
        else:
            return render(request, "create.html", {"form": form})
    else:
        form = ItemCreateForm()
        return render(request, "create.html", {"form": form})

@login_required()
def item_update(request, pk: int):
    item = Item.objects.get(pk=pk)
    if request.method == "POST":
        form = ItemUpdateForm(data=request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "post successfully updated")
            return redirect(reverse('liberty:detail', kwargs={"pk": item.id}))
        else:
            return render(request, "item_update.html", {"form": form})
    else:
        form = ItemUpdateForm(instance=item)
        return render(request, "item_update.html", {"form": form})


@login_required()
def item_delete(requet, pk):
    item = get_object_or_404(Item, pk=pk)
    if requet.method == "POST":
        messages.success(requet, "item successfully deleted")
        item.delete()
        return redirect(reverse('liberty:author', kwargs={"username": requet.user.username}))
    else:
        return render(requet, "item_delete.html", {"item": item})

class LikeItemView(LoginRequiredMixin, View):
    def get(self, request, pk):
        item = Item.objects.get(pk=pk)
        like, created = ItemLike.objects.get_or_create(user=request.user, item=item)
        if not created:
            like.delete()
        return redirect(reverse("liberty:category_list", kwargs={"pk": item.category.pk}))
