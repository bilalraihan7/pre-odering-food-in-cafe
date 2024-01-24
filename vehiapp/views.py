from django.shortcuts import render , redirect ,get_object_or_404
from .models import *
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import logout
from django.urls import reverse

def index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if User.objects.filter(email=email).exists():
            msg='User Already Exists'
            return render(request, 'vehiapp/index.html',{'msg':msg})
        else:

            user = User(name=name, email=email,password=password, image=image, address=address,
                        phone=phone)
            user.save()
            messages.success(request, 'User registration successful!')
            return redirect('/')
    else:

        a = vehicle.objects.all()
        return render(request, 'vehiapp/index.html',{'a':a})
def vehicles(request):
    a=vehicle.objects.all()
    return render(request,'vehiapp/vehicles.html',{"a":a})
def details_vehicle(request,pk):
    a = vehicle.objects.filter(id=pk)
    return render(request, 'vehiapp/single_vehicle.html', {"a": a})


def driver_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        license = request.FILES.get('license')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        if Driver.objects.filter(email=email).exists():
            msg='User Already Exists'
            return render(request, 'vehiapp/driverreg.html',{'msg':msg})
        else:
        
            driver = Driver(name=name, email=email, license=license, password=password, image=image, address=address, phone=phone)
            driver.save()
            messages.success(request, 'Driver registration successful!')
            return redirect('/')
    else:
        return render(request, 'vehiapp/driverreg.html')


def driver_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        license = request.FILES.get('license')
        password = request.POST.get('password')
        image = request.FILES.get('image')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        driver = Driver(name=name, email=email, license=license, password=password, image=image, address=address,
                        phone=phone)
        driver.save()
        messages.success(request, 'Driver registration successful!')
        return redirect('/')
    else:
        return render(request, 'vehiapp/driverreg.html')

def login(request):
    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')
        obj1 = Driver.objects.filter(email=email, password=password)
        obj2 = User.objects.filter(email=email, password=password)
        if obj1.filter(email=email, password=password).exists():
            for i in obj1:
                id = i.id
                status = i.status
                name=i.name
                request.session['email'] = email
                request.session['password'] = password
                request.session['id'] = id
                request.session['status'] = status
                request.session['name']=name
            # context ={'a': obj }
            if status == 'Verified':
                return redirect('http://127.0.0.1:8000/driver_home')
            else:
                msg='Your Account Verification Is Under Processing'
                return render(request, 'vehiapp/login.html',{'msg2':msg})
        elif obj2.filter(email=email, password=password).exists():
            for i in obj2:
                id = i.id
                name = i.name
                request.session['name'] = name
                request.session['email'] = email
                request.session['password'] = password
                request.session['id'] = id
                return redirect('http://127.0.0.1:8000/user_home')
        else:
            context = {'msg': 'Invalid Credentials'}
            return render(request,'vehiapp/login.html',context)
    return render(request, 'vehiapp/login.html')

def  view_license(request, id):
    provider = get_object_or_404(Driver, pk=id)
    if provider.license:
        image_path = provider.license.path
        with open(image_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='image/jpeg')
            response['Content-Disposition'] = f'inline; filename={provider.name}_license.jpg'
            return response
    else:
        return HttpResponse('License not found.')

def services(request):
    return render(request, 'vehiapp/services.html')

def user_home(request):
    id=request.session['id']
    user=User.objects.filter(id=id)
    vehicles=vehicle.objects.all()
    all_data={'user':user,'vehicles':vehicles}
    return render(request,'vehiapp/user_home.html', all_data )

def logout_view(request):
    logout(request)
    return redirect('/')

def driver_home(request):
    id=request.session['id']
    user=Driver.objects.filter(id=id)
    vehicles=vehicle.objects.filter(userid=id)
    all_data={'user':user,'vehicles':vehicles}
    return render(request,'vehiapp/driver_home.html', all_data )




def add_vehicle(request):
    if request.method == 'POST':
        vehicle_name = request.POST['vehicle_name']
        vehicle_reg = request.POST['vehicle_reg']
        vehicle_type = request.POST['vehicle_type']
        vehicle_image = request.FILES['vehicle_image']
        rate = request.POST['rate']
        user = request.session['id']
        driver=Driver.objects.get(id=int(user))
        
        new_vehicle = vehicle(userid=driver, vehicle_name=vehicle_name, vehicle_reg=vehicle_reg, vehicle_type=vehicle_type, vehicle_image=vehicle_image, rate=rate)
        new_vehicle.save()
        
        messages.success(request, 'Vehicle added successfully!')
        return redirect('/driver_home')
    id=request.session['id']
    user=Driver.objects.filter(id=id)
    return render(request, 'vehiapp/add_vehicle.html',{'user':user})

def delete_vehicle(request,id):
    a=vehicle.objects.get(id=id)
    a.delete()
    return redirect('/driver_home')

def filter(request,fid):
    id=request.session['id']
    user=Driver.objects.filter(id=id)
    vehicles=vehicle.objects.filter(vehicle_type=fid)
    all_data={'user':user,'vehicles':vehicles}
    return render(request,'vehiapp/filtered.html', all_data )


def search_vehicles(request):
    id=request.session['id']
    user=Driver.objects.filter(id=id)
    vehicle_name=request.GET.get('vehicle_name')
    result=vehicle.objects.filter(vehicle_name__icontains=vehicle_name)
    all_data={'user':user,'result':result}
    return render(request,'vehiapp/result.html', all_data )



def book_vehicle(request, vehicle_id):
    vehicles = vehicle.objects.get(id=vehicle_id)
    driver = vehicles.userid
    user_id = request.session['id']
    
    if request.method == 'POST':
        pickup_location = request.POST['pickup_location']
        dropoff_location = request.POST['dropoff_location']
        time = request.POST['time']
        date = request.POST['date']
        distance = request.POST['distance']
        user = User.objects.get(id=user_id)
        
        new_booking = booking.objects.create(
            user=user,
            driver=driver,
            vehicle=vehicles,
            pickup_location=pickup_location,
            dropoff_location=dropoff_location,
            time=time,
            date=date,
            distance=distance
        )
        
        vehicles.status = 'booked'
        vehicles.save()
        new_booking.save()
        
        messages.success(request, 'Your booking is confirmed!')
        
        # Redirect to payment page with booking ID
        return redirect(reverse('make_payment', args=[new_booking.id]))
    
    id = request.session['id']
    user = User.objects.filter(id=id)
    context = {'vehicle': vehicle, 'user': user}

    return render(request, 'vehiapp/book_vehicle.html', context)


def view_booking(request):
    id=request.session['id']
    bookings=booking.objects.filter(driver=id)
    user=Driver.objects.filter(id=id)
    all_data={'user':user,'bookings':bookings}
    return render(request,'vehiapp/viewbookings.html',all_data)



def view_drivers(request):
    id = request.session['id']
    user = User.objects.filter(id=id)
    drivers = Driver.objects.all()
    all_data = {'user': user, 'drivers': drivers}
    return render(request, 'vehiapp/drivers.html', all_data)

def my_booking(request):
    id=request.session['id']
    bookings=booking.objects.filter(user=id)
    user=User.objects.filter(id=id)
    all_data={'user':user,'bookings':bookings}
    return render(request,'vehiapp/mybookings.html',all_data)


def view_stats(request):
    countuser=User.objects.count()
    countdrivers=Driver.objects.count()
    countbookings=booking.objects.count()
    cvehicles=vehicle.objects.count()
    bookings = booking.objects.values('vehicle').annotate(total_bookings=Count('vehicle'))
    sorted_bookings = sorted(bookings, key=lambda x: x['total_bookings'], reverse=True)
    most_booked_id = sorted_bookings[0]['vehicle'] if sorted_bookings else None
    most_vehicle=vehicle.objects.filter(id=most_booked_id)


    all={
        'user':countuser,
        'driver':countdrivers,
        'bookings':countbookings,
        'vehicles':cvehicles,
        'most':most_vehicle
    }
    return render(request,'vehiapp/stats.html',all)


def make_payment(request, booking_id):
    if request.method == 'POST':
 
        book = get_object_or_404(booking, id=booking_id)
        payment_amount = book.distance * book.vehicle.rate if book.distance and book.vehicle else 0
        payment = Payment.objects.create(
            bookid=book,
            cname=request.POST.get('cname'),
            amount=payment_amount,
            cardno=request.POST.get('cardno'),
            cvv=request.POST.get('cvv')
        )

        book.payment = payment
        book.save()
        id=request.session['id']
        user = User.objects.filter(id=id)
        return render(request,'vehiapp/success.html',{'user':user})
    else:
        id = request.session['id']
        user = User.objects.filter(id=id)
        book = get_object_or_404(booking, id=booking_id)
        payment_amount = book.distance * book.vehicle.rate if book.distance and book.vehicle else 0
        return render(request, 'vehiapp/payment.html', {'user': user, 'payment_amount': payment_amount})

def edituser(request):
    if request.method == 'POST':
        id = request.session['id']
        user = User.objects.filter(id=id)
        up = User.objects.get(id=id)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if 'image' in request.FILES:
            image = request.FILES['image']
            up.image = image

        up.name = name
        up.address = address
        up.phone = phone
        up.email = email

        up.save()
        ud = User.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'user': user,
                   'msg': 'Profile Details Updated'}

        return render(request, 'vehiapp/editprofile-user.html', context)
    else:
        id = request.GET.get('id')
        id = request.session['id']
        up = User.objects.filter(id=id)
        user = User.objects.filter(id=id)
        all_data = {
            'user': user,
            'details': up,
        }
        return render(request, 'vehiapp/editprofile-user.html', all_data)

def changepassword_user(request):
    id = request.session['id']
    print(id)
    user = User.objects.filter(id=id)
    all = {
        'user': user,
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = User.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                msg =  'Password Changed Successfully'
                all = {
                    'user': user,
                    'msg': msg
                }
                return render(request, 'vehiapp/change_password_user.html',all)
            else:
                context =  'Your Old Password is Wrong'
                all = {
                    'user': user,
                    'msg': context
                }
                return render(request, 'vehiapp/change_password_user.html',all)

        except User.DoesNotExist:
            context =  'Your Old Password is Wrong'
            all = {
                'user': user,
                'msg': context
            }
            return render(request, 'vehiapp/change_password_user.html',all)
    else:
        return render(request, 'vehiapp/change_password_user.html',all)
    

def editdriver(request):
    if request.method == 'POST':
        id = request.session['id']
        user = Driver.objects.filter(id=id)
        up = Driver.objects.get(id=id)
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')

        if 'image' in request.FILES:
            image = request.FILES['image']
            up.image = image

        up.name = name
        up.address = address
        up.phone = phone
        up.email = email

        up.save()
        ud = Driver.objects.filter(email=request.session['email'])
        context = {'details': ud,
                   'user': user,
                   'msg': 'Profile Details Updated'}

        return render(request, 'vehiapp/editprofile-driver.html', context)
    else:
        id = request.GET.get('id')
        id = request.session['id']
        up = Driver.objects.filter(id=id)
        user =Driver.objects.filter(id=id)
        all_data = {
            'user': user,
            'details': up,
        }
        return render(request, 'vehiapp/editprofile-driver.html', all_data)

def changepassword_driver(request):
    id = request.session['id']
    print(id)
    user = Driver.objects.filter(id=id)
    all = {
        'user': user,
    }
    if request.method == 'POST':
        email = request.session['email']
        new_password = request.POST.get('new_password')
        current_password = request.POST.get('current_password')
        print('Email Is:' + email)
        print("Current_password" + str(current_password))
        try:

            ul = Driver.objects.get(email=email, password=current_password)

            if ul is not None:
                ul.password = new_password  # change field
                ul.save()
                msg =  'Password Changed Successfully'
                all = {
                    'user': user,
                    'msg': msg
                }
                return render(request, 'vehiapp/change_password_driver.html',all)
            else:
                context =  'Your Old Password is Wrong'
                all = {
                    'user': user,
                    'msg': context
                }
                return render(request, 'vehiapp/change_password_driver.html',all)

        except Driver.DoesNotExist:
            context =  'Your Old Password is Wrong'
            all = {
                'user': user,
                'msg': context
            }
            return render(request, 'vehiapp/change_password_driver.html',all)
    else:
        return render(request, 'vehiapp/change_password_driver.html',all)
    
def view_driver_vehicles(request,did):
    id = request.session['id']
    print(id)
    user = User.objects.filter(id=id)
    vehicl=vehicle.objects.filter(userid=did)
    driver=Driver.objects.filter(id=did)
    all_data={'user':user,'vehicle':vehicl,'driver':driver}
    return render (request,"vehiapp/user_view_driver_vehicles.html",all_data)
    