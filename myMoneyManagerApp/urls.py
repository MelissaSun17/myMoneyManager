from django.urls import path
from myMoneyManagerApp import views

app_name = 'myMoneyManager'

urlpatterns = [

    path('transaction/', views.get_transaction_list_self, name='transaction'),
    path('transaction_group/', views.get_transaction_list_group, name='transaction_group'),
    path('add_transaction/', views.add_single_transaction_self, name='add_single_transaction'),
    path('add_transaction_group/', views.add_single_transaction_group, name='add_single_transaction_group'),
    path('edit_transaction/', views.edit_single_transaction, name='edit_single_transaction'),
    path('delete_transaction/', views.delete_single_transaction, name='delete_single_transaction'),
    path('search_transaction/', views.search_transactions_self, name='search_transactions'),
    path('search_transaction_group/', views.search_transactions_group, name='search_transactions_group'),
    path('set_budget/', views.set_budget, name='set_budget'),
    path('user_login/', views.user_login, name='user_login'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('user_register/', views.register, name='register'),
    path('get_summary/', views.get_summary, name='get_summary'),
    path('create_group/', views.create_group, name='create_group'),
    path('add_member/', views.add_member, name='add_member'),
    path('delete_group/', views.delete_group, name='delete_group'),
    path('remove_member/', views.remove_member, name='remove_member'),
    path('get_members_by_group_id/', views.get_members_by_group_id, name='get_members_by_group_id'),



]
