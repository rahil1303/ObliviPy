Function PERMUTE(input_array A, bucket_size Z):
    N ← length(A)
    B ← ceil(N / Z)  // Number of buckets
    
    // Step 1: Assign each element a random bin ID
    for i in 0 to N-1:
        A[i].aux ← UniformRandom(0, B-1)
    
    // Step 2: Split elements into B buckets and pad each to size Z
    bucket[] ← array of B empty buckets
    for i in 0 to N-1:
        bucket[A[i].aux].append(A[i])
    
    for b in 0 to B-1:
        while length(bucket[b]) < Z:
            bucket[b].append(DummyElement)
    
    // Step 3: Perform log₂(B) rounds of merge-split routing
    rounds ← ⌈log₂(B)⌉
    for r in 0 to rounds-1:
        next_buckets ← []
        for i in 0 to length(bucket)-1 step 2:
            // Get bucket pair (handle odd length case)
            bucket_L ← bucket[i]
            bucket_R ← bucket[i+1] if i+1 < length(bucket) else array of Z dummies
            
            // Route elements based on r-th bit
            bucket0 ← []  // For elements where bit = 0
            bucket1 ← []  // For elements where bit = 1
            
            for elem in bucket_L + bucket_R:
                if elem is dummy:
                    bucket0.append(elem)
                else:
                    bit ← (elem.aux >> r) & 1
                    if bit == 0:
                        bucket0.append(elem)
                    else:
                        bucket1.append(elem)
            
            // Handle overflow condition
            if length(bucket0) > Z or length(bucket1) > Z:
                abort("Overflow detected")
            
            // Pad buckets to size Z
            while length(bucket0) < Z: bucket0.append(DummyElement)
            while length(bucket1) < Z: bucket1.append(DummyElement)
            
            next_buckets.append(bucket0)
            next_buckets.append(bucket1)
        
        bucket ← next_buckets
    
    // Step 4: Collect non-dummy elements and randomly shuffle
    result ← []
    for b in 0 to length(bucket)-1:
        for elem in bucket[b]:
            if elem is not dummy:
                result.append(elem)
    
    Shuffle(result)
    return result