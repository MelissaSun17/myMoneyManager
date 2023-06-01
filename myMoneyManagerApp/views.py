import datetime
import json
from django.contrib.auth import logout, login, authenticate
from django.core import serializers
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from myMoneyManagerApp.forms import TransactionForm
from myMoneyManagerApp.models import Transaction, Group, User
from myMoneyManagerApp.models import Budget
from django.views.decorators.http import require_http_methods


@require_http_methods(['GET'])
def get_transaction_list_self(request):
    response = {}
    try:
        # the self transaction part must provide a user id, i.e. no visitor access
        if request.GET['userId']:
            transaction = Transaction.objects.filter(transactionType=1) & Transaction.objects.filter(
                ownerId__contains=request.GET['userId'])
        else:
            transaction = None
        # Use paginator for paging.
        paginator = Paginator(transaction, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)  # If the passed page number is not an integer, return the first page
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)

        # serialize the paged transaction list and add to response.
        response['list'] = json.loads(serializers.serialize("json", page_obj))
        response['total_rows'] = len(transaction)
        response['current_page'] = int(page)
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def get_transaction_list_group(request):
    response = {}
    list = []
    try:
        # If a user id is provided, return all the group transactions the user belongs to.
        if request.GET.get('userId'):
            # get each value of the group ids that the user belongs to
            for groupId in User.objects.get(userId=request.GET['userId']).groupId.split(';'):
                if groupId == '':
                    break

                group = {}
                # get the transaction list for the group
                query = Transaction.objects.filter(groupId=groupId)
                paginator = Paginator(query, 10)
                page = request.GET.get('page')
                try:
                    page_obj = paginator.page(page)
                except PageNotAnInteger:
                    page_obj = paginator.page(1)  # If the passed page number is not an integer, return the first page
                except EmptyPage:
                    page_obj = paginator.page(paginator.num_pages)
                # return the information for paging, transaction list and group details.
                group.update({"total_rows": (len(query))})
                group.update({"current_page": (int(page))})
                group.update({"group_name": Group.objects.get(groupId=groupId).name})
                group.update({"group_id": groupId})
                group.update({"transactions": (json.loads(serializers.serialize("json", page_obj)))})
                list.append(group)
            response["list"] = list
        # If no user id is available i.e. a visitor, enter a group transaction by providing a group ID.
        elif request.GET.get('groupId'):

            groupId = request.GET['groupId']
            query = Transaction.objects.filter(groupId=groupId)
            paginator = Paginator(query, 10)
            page = request.GET.get('page')
            try:
                page_obj = paginator.page(page)
            except PageNotAnInteger:
                page_obj = paginator.page(1)  # If the passed page number is not an integer, return the first page
            except EmptyPage:
                page_obj = paginator.page(paginator.num_pages)
            is_paginated = True if paginator.num_pages > 1 else False  # If only one page, disable paging
            print(page_obj)
            response["list"] = {}
            # return the information for paging, transaction list and group details.
            response["list"].update({"total_rows": (len(query))})
            response["list"].update({"current_page": (int(page))})
            response["list"].update({"group_name": Group.objects.get(groupId=int(groupId)).name})
            response["list"].update({"group_id": groupId})
            response["list"].update({"transactions": (json.loads(serializers.serialize("json", page_obj)))})
    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1
    return JsonResponse(response)


@require_http_methods(['POST', 'GET'])
def add_single_transaction_self(request):
    form = TransactionForm()
    response = {}
    data = json.loads(request.body)
    if request.method == 'POST':
        form = TransactionForm(json.loads(request.body))

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new transaction to the database.
            transaction = form.save(commit=False)

            if data.get('userId'):
                transaction.ownerId = data.get('userId')
            transaction.createTime = datetime.datetime.now()
            transaction.transactionType = 1
            transaction.save()

            return HttpResponse('Success')
        else:
            print(form.errors)
            response['msg'] = str(form.errors)
    return HttpResponse(form.as_p())


def add_single_transaction_group(request):
    form = TransactionForm()
    response = {}
    data = json.loads(request.body)
    if request.method == 'POST':
        form = TransactionForm(json.loads(request.body))
        r = {}
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new transaction to the database.
            transaction = form.save(commit=False)
            if data.get('userId'):
                transaction.ownerId = data.get('userId')
            transaction.createTime = datetime.datetime.now()
            transaction.transactionType = 2

            if data.get('groupId'):
                transaction.groupId = data.get('groupId')
            transaction.save()

            return HttpResponse('Success')
        else:
            print(form.errors)
            response['msg'] = str(form.errors)
    return HttpResponse(form.as_p())


@require_http_methods(['POST'])
def edit_single_transaction(request):
    data = json.loads(request.body)
    transactionId = data.get('transactionId')
    category = data.get('category')
    values = data.get('values')
    description = data.get('description')
    type = Transaction.objects.filter(transactionId=transactionId).get().transactionType

    # Update the modifications by the user.
    Transaction.objects.filter(transactionId=transactionId).update(category=category, values=values,
                                                                   description=description)

    if type == 1:
        return HttpResponse({'msg': 'Self transaction added Success', 'success': True})
    else:
        return HttpResponse({'msg': 'Group transaction added Success', 'success': True})


@require_http_methods(['POST'])
def delete_single_transaction(request):
    data = json.loads(request.body)
    transactionId = data.get('transactionId')
    type = Transaction.objects.filter(transactionId=transactionId).get().transactionType
    Transaction.objects.filter(transactionId=transactionId).delete()
    if type == 1:
        return HttpResponse({'msg': 'Self transaction delete Success', 'success': True})
    else:
        return HttpResponse({'msg': 'Group transaction delete Success', 'success': True})


@require_http_methods(['GET'])
def search_transactions_self(request):
    response = {}
    # Receive the search keyword.
    keyword = request.GET['q']
    try:
        # keyword is a number , search through the description / category / values / ownerId fields.
        if keyword.isnumeric():
            transaction = Transaction.objects.filter(transactionType=1) & (
                    Transaction.objects.filter(description__contains=keyword) | Transaction.objects.filter(
                category=keyword) | Transaction.objects.filter(values=keyword)) & Transaction.objects.filter(
                ownerId__contains=request.GET['userId'])
        # keyword is a string ,only search across the description
        else:
            transaction = Transaction.objects.filter(description__contains=keyword) & Transaction.objects.filter(
                transactionType=1) & Transaction.objects.filter(ownerId__contains=request.GET['userId'])
        paginator = Paginator(transaction, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        is_paginated = True if paginator.num_pages > 1 else False
        response['list'] = json.loads(serializers.serialize("json", page_obj))
        response['total_rows'] = len(transaction)
        response['current_page'] = int(page)
        response['list'] = json.loads(serializers.serialize("json", transaction))

    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['GET'])
def search_transactions_group(request):
    response = {}
    keyword = request.GET['q']
    groupId = request.GET['groupId']
    try:
        # keyword is a number , search through the description / category / values / ownerId fields.
        if keyword.isnumeric():
            transaction = Transaction.objects.filter(transactionType=2) & (
                    Transaction.objects.filter(description__contains=keyword) | Transaction.objects.filter(
                category=keyword) | Transaction.objects.filter(values=keyword)) & Transaction.objects.filter(
                groupId=groupId)
        # keyword is a string ,only search across the description
        else:
            transaction = Transaction.objects.filter(description__contains=keyword) & Transaction.objects.filter(
                transactionType=2) & Transaction.objects.filter(
                groupId=groupId)
        paginator = Paginator(transaction, 10)
        page = request.GET.get('page')
        try:
            page_obj = paginator.page(page)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        is_paginated = True if paginator.num_pages > 1 else False
        response['list'] = json.loads(serializers.serialize("json", page_obj))
        response['total_rows'] = len(transaction)
        response['current_page'] = int(page)


    except Exception as e:
        response['msg'] = str(e)
        response['error_num'] = 1

    return JsonResponse(response)


@require_http_methods(['POST'])
def set_budget(request):
    data = json.loads(request.body)
    userId = data.get('userId')
    setBudget = data.get('setBudget')
    try:
        budget, created = Budget.objects.get_or_create(ownerId=userId,
                                                       defaults={'setBudget': 0, 'startDate': datetime.datetime.now(),
                                                                 'modifyTime': datetime.datetime.now()})
        budget.setBudget = setBudget
        budget.startDate = datetime.datetime.now()
        budget.modifyTime = datetime.datetime.now()

        budget.save()

        return JsonResponse({'success': 'Budget set successfully'})
    except Exception as e:
        return JsonResponse({'msg': str(e), 'error_num': 1})


@require_http_methods(['POST'])
def user_logout(request):
    logout(request)
    return JsonResponse({'success': True})


@require_http_methods(['POST'])
def user_login(request):
    # get form information
    data = json.loads(request.body)

    email = data.get('email')
    password = data.get('password')

    # authenticate user
    user = authenticate(username=email, password=password)
    # user = User.objects.get(userId=3)
    if user is not None:
        login(request, user)
        user.password = ''
        user_serialized = serializers.serialize('json', [user, ])
        return JsonResponse({'success': True, 'result': user_serialized}, safe=False)
        # return JsonResponse({'success': True, 'result': serializers.serialize("json", user)})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid login credentials'})


@require_http_methods(['POST'])
def get_members_by_group_id(request):
    # get form information
    data = json.loads(request.body)
    groupId = data.get('groupId')

    group = Group.objects.get(groupId=groupId)
    emails = group.email_list.split(';')
    emails = emails[:-1]
    memberInfo = User.objects.filter(email__in=emails).values('userId', 'username', 'email')
    if memberInfo:
        userEmails = [info['email'] for info in memberInfo]
        visitorEmails = [x for x in emails if x not in userEmails]
        visitorInfo = [{'userId': -1, 'username': 'visitor', 'email': email} for email in visitorEmails]
        memberInfo = list(memberInfo) + visitorInfo
        return JsonResponse({'success': True, 'result': json.dumps(memberInfo)})
    else:
        return JsonResponse({'success': False, 'error': 'no members'})


@require_http_methods(['POST'])
def get_summary(request):
    # get form information
    data = json.loads(request.body)
    userId = data.get('userId')

    # authenticate user
    budgets = None
    if userId:
        transactions = Transaction.objects.filter(ownerId=userId)
        try:
            budgets = Budget.objects.get(ownerId=userId)
        except Exception as e:
            print(e)
        if budgets is not None:
            budget = budgets.setBudget
        else:
            budget = 0
        total_expense = groceries = charity = eating_out = entertainment = general = transport = other = 0
        if transactions:
            for transaction in transactions:
                total_expense += transaction.values
                if transaction.category == 1:
                    groceries += transaction.values
                elif transaction.category == 2:
                    charity += transaction.values
                elif transaction.category == 3:
                    eating_out += transaction.values
                elif transaction.category == 4:
                    entertainment += transaction.values
                elif transaction.category == 5:
                    general += transaction.values
                elif transaction.category == 6:
                    transport += transaction.values
                else:
                    other += transaction.values
        result = {'total_expense': total_expense,
                  'detail': [{'category': 1, 'value': groceries}, {'category': 2, 'value': charity},
                             {'category': 3, 'value': eating_out},
                             {'category': 4, 'value': entertainment}, {'category': 5, 'value': general},
                             {'category': 6, 'value': transport}, {'category': 7, 'value': other}], 'budget': budget}
        return JsonResponse({'success': True, 'result': result}, safe=False)
    else:
        return JsonResponse({'success': False, 'error': 'get summary failed: invalid userId'})


def register(request):
    if request.method == 'POST':
        # Get form information

        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        email = data.get('email')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, 'Inconsistent of twice password inputs!')
            return redirect('register')

        # Create new user and save to database
        user = User.objects.create_user(username=username, password=password, email=email, totalExpenses=0, status=0,
                                        role=1)
        user.save()

        # Log in the new user and redirect to the home page
        messages.success(request, 'Register success！')
        return HttpResponse('Success')

    # Render the registration page
    return redirect('register')


def create_group(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_name = data.get('name')
        admin_id = data.get('userId')  # assuming user is logged in and authenticated
        user = User.objects.get(userId=admin_id)
        user_email = user.email
        # Create a new Group object with the given name and admin ID
        new_group = Group.objects.create(name=group_name, adminId=admin_id, billList='',
                                         numMembers=1, memberIds=str(admin_id) + ';', email_list=user_email + ";")
        # Add the new group to the current user's group list
        current_user = User.objects.get(userId=admin_id)
        current_user.groupId += str(new_group.groupId) + ';'
        current_user.save()
        # Return a JSON response with the new group's ID
        response_data = {'groupId': new_group.groupId}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse('Invalid Request')


def add_member(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('groupId')
        email = data.get('email')

        # Find the user with the specified email, or create a new user
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Retrieve the group object
        group = Group.objects.get(groupId=group_id)

        # Check if the current user is the administrator of the group
        current_user_id = data.get('userId')
        if group.adminId != current_user_id:
            response_data = {'message': 'Only the administrator can add members to the group.'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        # Add the email to the group's email list
        if group.email_list:
            group.email_list += email + ';'
        else:
            group.email_list = email + ';'
        group.save()

        # If a matching user was found, add the user to the group
        added_members = []
        if user:
            # Update the group's memberIds field to include the new member's ID
            if group.memberIds:
                group.memberIds += str(user.userId) + ';'
            else:
                group.memberIds = str(user.userId) + ';'
            group.numMembers += 1
            group.save()

            # Update the user's groupId field to include the new group's ID
            if user.groupId:
                user.groupId += str(group_id) + ';'
            else:
                user.groupId = str(group_id) + ';'
            user.save()

            # Add the user's email to the list of added members
            added_members.append({'email': email, 'userId': user.userId})

        # Split the email list and return it as a response
        email_list = group.email_list.split(';')
        response_data = {'message': 'Member added successfully.', 'addedMembers': added_members,
                         'emailList': email_list}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    else:
        return HttpResponse('Invalid Request')


def delete_group(request):
    # Get the group object
    data = json.loads(request.body)
    group_id = data.get('groupId')
    group = Group.objects.get(groupId=group_id)
    current_user_id = data.get('userId')
    if group.adminId != current_user_id:
        response_data = {'message': 'Only the administrator can remove members from the group.'}
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    # Remove the group ID from all users' groupId field
    for member_id in group.memberIds.split(';'):
        if member_id:
            user = User.objects.get(userId=member_id)
            if user.groupId:
                ids = user.groupId.split(';')
                if str(group_id) in ids:
                    ids.remove(str(group_id))
                    user.groupId = ';'.join(ids)
                    user.save()

    # Delete the group from the database
    group.delete()
    # Return a success message
    response_data = {'success': True}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


def remove_member(request):
    # Check if the request method is POST
    if request.method == 'POST':
        data = json.loads(request.body)
        group_id = data.get('groupId')
        email = data.get('email')

        # Find the user with the specified email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        # Retrieve the group object
        group = Group.objects.get(groupId=group_id)

        # Check if the current user is the administrator of the group
        current_user_id = data.get('userId')
        if group.adminId != current_user_id:
            response_data = {'message': 'Only the administrator can remove members from the group.'}
            return HttpResponse(json.dumps(response_data), content_type='application/json')

        # Check if the email is in the emaillist
        if email in group.email_list:
            # Remove the email from the group's emaillist field
            group.email_list = group.email_list.replace(email + ';', '')
            # Save the group object
            group.save()

            if user and str(user.userId) + ';' in group.memberIds:
                # Remove the member's ID from the group's memberIds field
                group.memberIds = group.memberIds.replace(str(user.userId) + ';', '')
                # Decrement the number of members in the group
                group.numMembers -= 1
                # Save the group object
                group.save()

                # Check if the group is in the user's groupId field
                if str(group_id) + ';' in user.groupId:
                    # Remove the group's ID from the user's groupId field
                    user.groupId = user.groupId.replace(str(group_id) + ';', '')
                    # Save the user object
                    user.save()

            # Get the list of emails in the group's emaillist field
            email_list = group.email_list.split(';')
            # Return a success response with the email list
            response_data = {'message': 'Member removed successfully.', 'emailList': email_list}
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse('User not in the group')
    else:
        # If the request method is not POST, return an invalid request
        return HttpResponse('Invalid Request')
