from django.contrib import admin

from .models import User, Item, UserLike, Category, ItemLike


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "username", "like_count", "password"]
    search_fields = ["first_name", "username", "last_name"]
    # list_filter = ["post_count",]
    list_display_links = ["username", "password"]
    def get_like_count(self):
        return self.get_like_count()


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ["title", "description", "author", "category", "ends_in", "created_at", "updated_at", "price", "owner_name", "owner_username"]
    search_fields = ["title", "author"]
    list_filter = ["author", "category", "ends_in"]
    date_hierarchy = "ends_in"

@admin.register(UserLike)
class UserLikeAdmin(admin.ModelAdmin):
    list_display = ["user", "author"]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]

    class Meta:
        verbose_name_plural = "Categories"
        verbose_name = "Category"
@admin.register(ItemLike)
class ItemLikeAdmin(admin.ModelAdmin):
    list_display = ["Item"]