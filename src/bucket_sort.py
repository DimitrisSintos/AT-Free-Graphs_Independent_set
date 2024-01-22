class BucketSort:
    def __init__(self, input_list, key_function):
        self.input_list = input_list
        self.key_function = key_function  # Function to get the value to sort by (e.g., len)
        
    def sort(self):
        max_value = max(self.input_list, key=self.key_function)
        max_len = self.key_function(max_value)
        
        # Create n empty buckets where n is the max length
        buckets = [[] for _ in range(max_len + 1)]
        
        # Distribute input elements into buckets
        for item in self.input_list:
            length = self.key_function(item)
            buckets[length].append(item)
        
        # Concatenate buckets with sorted elements into a single list
        sorted_list = []
        for bucket in buckets:
            for item in sorted(bucket, key=self.key_function):  # Using built-in sort for individual buckets
                sorted_list.append(item)
        return sorted_list
