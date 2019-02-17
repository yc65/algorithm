//
//  main.c
//  counting_inversion
//
//  Created by yc65 on 2018/12/22.
//  Copyright © 2018 yc65. All rights reserved.
//

#include <stdio.h>
#include <stdlib.h>

int merge_and_count_split_inv(int inp_array[], int temp_array[], int left, int mid, int right);

int sort_and_count(int inp_arr[], int temp_arr[], int left, int right)
{
    int count_inv = 0;
    int mid = 0;

    if(left<right)
    {
        mid = (int) (left+right)/2;
        count_inv+=sort_and_count(inp_arr, temp_arr, left, mid);
        count_inv+=sort_and_count(inp_arr, temp_arr, mid+1,right);
        count_inv+=merge_and_count_split_inv(inp_arr, temp_arr, left, mid, right);
    }
    return count_inv;
}

int merge_and_count_split_inv(int inp_array[], int temp_array[], int left, int mid, int right)
{
    // mid is the last of the first half of the array
    int i = left;
    int j = mid+1;
    int k = left;
    int count_inv = 0;
    
    while (i<=mid && j <= right)
    {
        if (inp_array[i]<inp_array[j])
        {
            temp_array[k] = inp_array[i];
            i++;
            k++;
        }
        else
        {
            temp_array[k] = inp_array[j];
            count_inv = count_inv + mid-i+1;
            j++;
            k++;
        }
    }
    
    while (i<=mid)
    {
        temp_array[k] = inp_array[i];
        i++;
        k++;
    }
    
    while (j<=right)
    {
        temp_array[k] = inp_array[j];
        j++;
        k++;
    }
    
    for (i=left; i<=right; i++)
    {
        inp_array[i] = temp_array[i];
    }
    
    return count_inv;
}

int main(int argc, const char * argv[]) {
    // insert code here...
    int *temp = NULL;
    int inv_count;
    int array_size = 8;
    int input_array[8] = {1, 3, 7, 9, 5, 2, 4, 6};
    temp = (int *)malloc(sizeof(int)*8);
    
    inv_count = sort_and_count(input_array, temp, 0, array_size-1);
    printf("The result is %d \n", inv_count);
    if(temp!=NULL)
    {
        free(temp);
    }
    return 0;
}
