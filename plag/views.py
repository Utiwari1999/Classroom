from django.shortcuts import render
from .forms import UploadFileForm
from django.http import HttpResponseRedirect
from .process_file import process_file,compare_two
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
        c,output = process_file(myfile)
        render_obj = []
        for ele in sorted(output.items(),key=operator.itemgetter(1),reverse=True):
            if c[ele[0]]*100 > 20 and ele[1]>1:
                render_obj.append([ele[1],ele[0],round(c[ele[0]]*100.00,2)])
                
        return render(request, 'output.html', {
            'render_obj': render_obj,
            'filename' : name,
        })
    return render(request, 'index.html',{'message':"Hello World"})


def compare_files(request):
    if request.method == 'POST' and request.FILES['myfile1'] and request.FILES['myfile2']:
        myfile1 = request.FILES['myfile1']
        myfile2 = request.FILES['myfile2']
        label1 = request.POST.get('label1')
        label2 = request.POST.get('label2')
        

        fs = FileSystemStorage()
        if myfile1.name.endswith('.txt'):
            label1 = label1 + '.txt'
        elif myfile1.name.endswith('.pdf'):
            label1 = label1 + '.pdf'
        else:
            label1 = label1 + '.docx'

        filename1 = fs.save(label1, myfile1)
        
        fs = FileSystemStorage()
        if myfile2.name.endswith('.txt'):
            label2 = label2 + '.txt'
        elif myfile2.name.endswith('.pdf'):
            label2 = label2 + '.pdf'
        else:
            label2 = label2 + '.docx'
        filename2 = fs.save(label2, myfile2)
        # compare_two(myfile1,myfile2)
        line1,line2,pos1,pos2,dataA,dataB = compare_two(myfile1,myfile2)
        print(pos1)
        print(pos2)
        liA = []
        prev_pos = 0
        pos1.sort()
        for i,j in pos1:
            # i,j = int(i),int(j)

            liA.append([dataA[prev_pos:i],0]) 
            liA.append([dataA[i:j],1])
            prev_pos = j
        liA.append([dataA[prev_pos:],0])
        
        pos2.sort()
        liB = []
        prev_pos = 0
        for i,j in pos2:
            # i,j = int(i),int(j)
            liB.append([dataB[prev_pos:i],0]) 
            liB.append([dataB[i:j],1])
            prev_pos = j
        liB.append([dataB[prev_pos:],0])

        return render(request, 'success.html', {
            'data1': liA,
            'data2': liB,
            'filename1' : label1,
            'filename2' : label2,
        })
    return render(request, 'file_compare.html')
