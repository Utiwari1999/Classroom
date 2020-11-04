from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from .process_file import process_file
from django.core.files.storage import FileSystemStorage
import operator
# Imaginary function to handle an uploaded file.



def upload_file(request):
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        name = request.POST.get('name')
        fs = FileSystemStorage()
        if myfile.name.endswith('.txt'):
            name = name + '.txt'
        else:
            name = name + '.docx'
        filename = fs.save(name, myfile)
        uploaded_file_url = fs.url(filename)
        c,output = process_file(myfile)
        render_obj = []
        for ele in sorted(output.items(),key=operator.itemgetter(1),reverse=True):
            if c[ele[0]]*100 > 20 and ele[1]>1:
                render_obj.append([ele[1],ele[0],c[ele[0]]*100.00])
                
        return render(request, 'success.html', {
            'render_obj': render_obj,
            'filename' : name,
        })
    return render(request, 'index.html',{'message':"Hello World"})


def compare_files(request):
    if request.method == 'POST' and request.FILES['myfile1'] and request.FILES['myfiles2']:
        myfile1 = request.FILES['myfile1']
        myfile2 = request.FILES['myfile2']
        label1 = request.POST.get('label1')
        label2 = request.POST.get('label2')
        # fs = FileSystemStorage()
        # if myfile.name.endswith('.txt'):
        #     name = name + '.txt'
        # else:
        #     name = name + '.docx'
        # filename = fs.save(name, myfile)
        # uploaded_file_url = fs.url(filename)
        # c,output = process_file(myfile)
        # render_obj = []
        # for ele in sorted(output.items(),key=operator.itemgetter(1),reverse=True):
        #     if c[ele[0]]*100 > 20 and ele[1]>1:
        #         render_obj.append([ele[1],ele[0],c[ele[0]]*100.00])
                
        # return render(request, 'success.html', {
        #     'render_obj': render_obj,
        #     'filename' : name,
        # })


        print(myfile1.name,myfile2.name)
    return render(request, 'file_compare.html',{'message':"Hello World"})
