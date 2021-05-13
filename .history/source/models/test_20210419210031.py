def binarySearch(arr,target):
    low = 0
    high = len(arr)-1
    close = -1
    while low<=high:
        mid = low+(high-low)//2
        if arr[mid]>=target:
            high = mid-1
        elif arr[mid]<target:
            close = mid
            low = mid+1
    return close

def triangle(nums):
    if len(nums)<3:
        return 0

    nums.sort()
    p1,p2,p3 = 0,1,2
    count = 0
    for i in range(len(nums)-1):
        target = nums[i]+nums[i+1]
        if i+2<len(nums):
            ind = binarySearch(nums,target)
            if ind != -1:
                print(nums[i],nums[i+1],nums[i+2:ind])
                count += ind

    return count

nums = [2,2,4,3]
print(triangle(nums))