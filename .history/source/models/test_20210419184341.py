def triangle(nums):
    if len(nums)<3:
        return 0

    nums.sort()
    p1,p2,p3 = 0,1,2
    count = 0
    while p1<p2 and p2<p3 and p3<len(nums):
        print(p1,p2,p3)
        if nums[p1]+nums[p2]>nums[p3]:
            #print(nums[p1],nums[p2],nums[p3])
            while p1<p2 and p2<p3:
                if nums[p1]+nums[p2]>nums[p3]:  
                    #print(nums[p1],nums[p2],nums[p3]) 
                    count += 1
                p1+=1
            p2 += 1
            
        else:
            p3 += 1
    return count

nums = [10,10,11,12,13,14,15,16,17,17,18,19,20,21]
print(triangle(nums))