from django.template.response import TemplateResponse
from django.http import HttpResponse
from .models import User_Data,Category,SubCategory,Attributes,Product_attribute
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
session = []

def admin(request):
    return render(request,'admin.html')

def homepage(request):
    queryset = Category.objects.all()
    return render(request,"homepage.html",{"category_data" : queryset})

def signup(request):
    return render(request,"signup.html")

def checkEmailandPassword(request):
    email = request.POST['uemail']
    password = request.POST['upassword']
    confirmpassword = request.POST['cpassword']
    user = User_Data.objects.filter(user_email=email)
    if user.count() == 0:
        if password == confirmpassword:
            return addUser(request)
        else:
            passwordError = "Both Password should match."
            return TemplateResponse(request, "signup.html", {"Error": passwordError})
    else:
        emailError = "Email address already exists."
        return TemplateResponse(request, "signup.html", {"Error": emailError})

def onaddCategoryclick(request):
    cats = Category.objects.all()
    if session:
       session[:] = []
    return render(request,'onaddCategoryclick.html',{'cats':cats})

def saveCategory(request):
    if request.method == 'POST':
        radio = request.POST.get('optradio',None)
        if radio == 'existing':
            category = request.POST.get('cat_option',None)
            cat = Category.objects.filter(cat_name=category)
            cat_message=""
            subcategory = request.POST.get('sub_cat', None)
            subcatobj = SubCategory(subcat_name=subcategory,category_id=cat[0].cat_id)
            subcatobj.save()
            subcat_message = subcategory+" Added.."
            att_message=""
            for x in session:
                att_value = x
                attobj = Attributes(attribute_name=att_value,subcategory_id=subcatobj.subcat_id)
                attobj.save()
                att_message = att_message+" "+x+" att added"
            msg_list={cat_message,subcat_message,att_message}
            return render(request,'result.html',{'msg_list':msg_list})
        if radio == 'new':
            category = request.POST.get('new_cat',None)
            catobj = Category(cat_name=category)
            catobj.save()
            cat_message = category+" Added"
            subcategory = request.POST.get('sub_cat', None)
            subcatobj = SubCategory(subcat_name=subcategory,category_id=catobj.cat_id)
            subcatobj.save()
            subcat_message = subcategory+" Added.."
            att_message=""
            for x in session:
                att_value = x
                attobj = Attributes(attribute_name=att_value,subcategory_id=subcatobj.subcat_id)
                attobj.save()
                att_message = att_message+" "+x+" att added. "
            msg_list = {cat_message,subcat_message,att_message}
            return render(request,'result.html',{'msg_list':msg_list})

@csrf_exempt
def addtosession(request):
    att_value = request.POST['myvalue']
    if not att_value in session:
        session.append(att_value)
        request.session[att_value] = att_value
        return HttpResponse(att_value+" added..")
    else:
        return HttpResponse("Attribute already added.!")

@csrf_exempt
def deletefromsession(request):
    att_value = request.POST['myvalue']
    if att_value in session:
        session.remove(att_value)
        del request.session[att_value]
        return HttpResponse(att_value+" deleted..")
    else:
        return HttpResponse("Attribute Not found..!")

def addUser(request):
    if request.method == 'POST':
        username = request.POST['uname']
        lastname = request.POST['usurname']
        email = request.POST['uemail']
        password = request.POST['upassword']
        confirmpassword = request.POST['cpassword']
        phone_no = request.POST['uphonenumber']
        userdata = User_Data(first_name=username ,last_name=lastname,user_email=email,user_password=password,user_phone_no=phone_no)
        userdata.save()
        return TemplateResponse(request,"login.html",{})

def login(request):
    return render(request,'login.html')

def loginValidation(request):

    email_id = request.POST['uemail']
    password = request.POST['upassword']

    user = User_Data.objects.filter(user_email = email_id)

    correct_password = user[0].user_password

    if password == correct_password:
        if email_id == 'admin@gmail.com':
            return render(request, 'admin.html')
        else:
            successMessage = "You are successfully logged in."
            return TemplateResponse(request, "homePage.html", {"Success": successMessage})
    else:
        errorMessage = "Invalid credentials inserted"
        return TemplateResponse(request, "login.html", {"Success": errorMessage})

def ondeletecategoryclick(request):
    cat=Category.objects.all()
    sub_cat=SubCategory.objects.all()
    att=Attributes.objects.all()
    return render(request,'deletecategory.html',{'cat':cat,'sub_cat':sub_cat,'att':att})
	
@csrf_exempt
def delete_att(request):

    return HttpResponse("Response..!!")