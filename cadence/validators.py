
def cadence_import_args_validator(request,url,args):

    flag = True
    if(url[:8]!="https://"):
        flag = False
        messages.error(request,"invalid url")
    
    for arg in args:
        if(arg<0):
            flag = False
            messages.error(request, "args can't be negative")
            break
    if(not flag):
        return redirect("cadence:cadence-detail") 

