insert(value):
	if((rear + 1) % 5 == 0):
		rear = 0
	else:
		rear++

	int x1 = value;
	for(int i = front; i == rear; i++):
		if(!(x2 > array[i])):
			int temp = array[i]
			array[i] = x2
			x2 = temp

		if(i % 5 == 0):
			i = 0

	array[rear] = x1