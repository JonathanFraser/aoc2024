import numpy as np

with open('inputs/day9.txt') as f:
    arr = np.array([ int(r) for r in f.read().strip()])

N = arr.sum()
blocks = np.ndarray((N,),dtype=int)
blocks[:]=-1
ptr = 0 
free_space = []
files = []
for (i,v) in enumerate(arr):
    if i % 2 == 0:
        file_id = i//2
        blocks[ptr:ptr+v] = file_id
        files.append((ptr,v,file_id))
    else:
        free_space.append((ptr,v))
        blocks[ptr:ptr+v] = -1
    ptr += v


start_ptr = 0 
end_ptr = N-1
while start_ptr < end_ptr:
    if blocks[start_ptr] != -1:
        start_ptr += 1
        continue
    
    if blocks[end_ptr] == -1:
        end_ptr -= 1
        continue

    blocks[start_ptr] = blocks[end_ptr]
    blocks[end_ptr] = -1
    start_ptr += 1
    end_ptr -= 1

blocks[blocks == -1] = 0
print(np.sum(np.arange(0,N)@blocks))

files.reverse()

for (i,(f_ptr,f_size,f_id)) in enumerate(files):
    for (j,(sp_ptr,sp_size)) in enumerate(free_space):
        if sp_ptr > f_ptr:
            break

        if sp_size >= f_size:
            files[i] = (sp_ptr,f_size,f_id)
            free_space[j] = (sp_ptr+f_size,sp_size-f_size)
            break

f_blocks = np.ndarray((N,),dtype=int)
f_blocks[:]=0
for (f_ptr,f_size,f_id) in files:
    f_blocks[f_ptr:f_ptr+f_size] = f_id

for (sp_ptr,sp_size) in free_space:
    f_blocks[sp_ptr:sp_ptr+sp_size] = 0 

print(np.sum(np.arange(0,N)@f_blocks))


        
