tc = "000000111110100"
tc = list(tc)

n = len(tc)

for i in range(1,n-1):
    if(tc[i-1]=="1" and tc[i]=="0" and tc[i+1]=="1"):
        tc[i] = "1"

print(tc)
curr_pos = 0

count = 0
while(curr_pos<n-1):
    if(tc[curr_pos+1]=="0"):
        curr_pos+=1
        
    elif(tc[curr_pos+3]=="0"):
        curr_pos+=3
        
    
    else:
        while(tc[curr_pos+1]=="1"):
            count+=1
            curr_pos+=1
    
            
                  
print(count+1)