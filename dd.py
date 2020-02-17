print(2)

# def count_even(num_list):

# """Counts how many even numbers there are in a list.
# Args:
# num_list (list): List of numbers to be checked.
# Returns:
#  int: The count of even numbers in the list."""

# num_list = [7, 65, 1337, 8, -2, 24, 6, 67, 54, 36, 25, 1, 42, 9, 138, 4356, 6] # should be supplied, not defined
# 	even_numbers = [] 
# 	for i in num_list:
# 		if i % 2 == 0:
# 			even_numbers.append(i)
# 			# opportunity on this line to print i, which is a number that just passed the even number test. consider doing so as a string like str(i). just good practice, print won't complain as is but when doing things like print("i am "  + 6 + " feet tall"), it won't like it. only a one-off number will it convert for you.
# 			# ...cont: the end result in the terminal will be what you need, OR if you need to do it separately (ex reasoning: you add another print in the loop so now the output will be interuppted, be janky, and non useful)
# 		return even_numbers # the indentation here has your return statement inside the loop checking each number for even-ness. at the end of it, but still inside it. moved back to the indentation of the 'for i in...' will have it execute after you have the list of evens built BUT... i see above, this function is supposed to return the count of evens, not the list, so...
# 	print(even_numbers([7, 65, 1337, 8, -2, 24, 6, 67, 54, 36, 25, 1, 42, 9, 138, 4356, 6])) # not sure what stage or step this print was meant for, but being after the return in a function means its outside of the funcction, which importantly means that it doesn't know about stuff inside of it, like your even_list
   

# changed up a bit...
# num_list = [7, 65, 1337, 8, -2, 24, 6, 67, 54, 36, 25, 1, 42, 9, 138, 4356, 6] # outside the function, (above) so it will be known to everything in the module (read: entirety of the code in this py file)

# def new_count_even(num_list):

# 	even_number_count = 0 # a count instead, like the docstring (description stuff below the def count_even... line in your post) promises. start it at zero
# 	for i in num_list:
# 		if i % 2 == 0:
# 			even_numbers += 1 # a fancy, slightly sexy way of adding 1 to whatever even_numbers is, and setting it equal to that. boring way: even_numbers = even_numbers + 1 

# 	return even_number_count # return the count, as promised. will be zero like when we created it if no even numbers were given.

# # and finally, the thing you wanted (print the even numbers) in case you didn't need any of the stuff up above. again, i changed it because of its unexpected behaviour given its function description. in case it was the description that was wrong, or both, heres one that takes a list and returns one, with only the evens AND prints it for you (a few ways once again, your option which to keep)

# def only_even_numbers(num_list):

# 	even_numbers = [] 
# 	for i in num_list:
# 		if i % 2 == 0:
# 			even_numbers.append(i)
# 			print(str(i)) # option 1

# 	for number in even_numbers: # option 2, which is just an important bit of logic you will use again and just did above: list iteration
# 		print(number       eg)

# 	# option 3 : one liner, using whats called list comprehension. essence here is i want to print each thing in the list but the string version of it.
# 	print(str(i) for i in even_numbers)

my_list = [1,2,3,4,5,6,7,8,10]


print([(num%2==0) or num for num in my_list])
	
