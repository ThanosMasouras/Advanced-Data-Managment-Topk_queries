import sys
import heapq

def get_next_obj(line):
    id, score = line.split()
    id = int(id)
    score = float(score)

    return id,score

def read_rnd():
    R = {}
    with open("rnd.txt", "r") as rnd_file:
        for line in rnd_file:
            obj_id, score = line.split()
            R[int(obj_id)] = float(score)

    return R

def create_heap_Wk(lower_bounds,k):
    Wk = []
    # sort lower bounds by score in descending order
    sorted_lower_bounds = sorted(lower_bounds.items(), key=lambda x: x[1] or 0, reverse=True)
    # get the top k objects based on their sorted lower bounds
    top_k_objs = sorted_lower_bounds[:k]
    # convert the top k objects to a heap format with object ID and score
    for obj in top_k_objs:
        heapq.heappush(Wk, (obj[1], obj[0]))

    return Wk

def print_result(n, Wk):
    print(f"Number of sequential accesses= {n}")
    print("Top k objects:")
    Wk = heapq.nlargest(len(Wk), Wk)
    for obj in Wk:
        score, id = obj
        print(f"{id}: {score:.2f}")

def top_k_scores(k): 
    objs_checked = 0
    T = 0 
    wk_created = 0
    lower_bounds = {}
    total_scores = {}
    objs_seq1 = []
    objs_seq2 = [] 
    sequential_accesses = 0
    terminate = False
    R = read_rnd()
    seq1_file = open("seq1.txt", "r")
    seq2_file = open("seq2.txt", "r")
    
    while True:

        # Get the next object id and score
        seq1_line = seq1_file.readline()
        seq2_line = seq2_file.readline()
        seq1_obj_id, seq1_score = get_next_obj(seq1_line)
        seq2_obj_id, seq2_score = get_next_obj(seq2_line)


        # Calculate the new threshold for the next iteration
        T = round(seq1_score + seq2_score + 5.00,2)
        sequential_accesses += 2

        # If the object id from sequence 1 is already in lower bounds, add the score to its total score
        # Otherwise, add the score to the object's R value and add the object id to the list of checked objects from sequence 1
        if seq1_obj_id in lower_bounds:
            total_scores[seq1_obj_id] = round(lower_bounds[seq1_obj_id] + seq1_score,2)
        else:
            objs_checked += 1
            lower_bounds[seq1_obj_id] = round(R[seq1_obj_id] + seq1_score,2)
            objs_seq1.append(seq1_obj_id)

        # If the number of checked objects equals k, create the Wk heap
        if wk_created == 0 and objs_checked == k:
            Wk = create_heap_Wk(lower_bounds,k)
            wk_created = 1

        # If the Wk heap exists and the object id from seq1 is already in the total scores dictionary, 
        # check if its score is greater than the lowest score in the heap
        # If it is, replace the lowest score in the heap with the object's score
        if wk_created == 1 and seq1_obj_id in total_scores: 
            smallest_score = heapq.heappop(Wk)
            if total_scores[seq1_obj_id] > smallest_score[0]:
                heapq.heappush(Wk,(total_scores[seq1_obj_id],seq1_obj_id))
            else:
                heapq.heappush(Wk,smallest_score)

        # If the object id from seq2 is already in lower bounds, add the score to its total score
        # Otherwise, add the score to the object's R value and add the object id to the list of checked objects from sequence 2
        if seq2_obj_id in lower_bounds:
            total_scores[seq2_obj_id] = round(lower_bounds[seq2_obj_id] + seq2_score,2)
        else:
            objs_checked += 1
            lower_bounds[seq2_obj_id] = round(R[seq2_obj_id] + seq2_score,2)
            objs_seq2.append(seq2_obj_id)

        # If the number of checked objects equals k, create the Wk heap
        if wk_created == 0 and objs_checked == k:
            Wk = create_heap_Wk(lower_bounds,k)
            wk_created = 1

        # If the Wk heap exists and the object id from seq2 is already in the total scores dictionary, 
        # check if its score is greater than the lowest score in the heap
        # If it is, replace the lowest score in the heap with the object's score
        if wk_created == 1 and seq2_obj_id in total_scores: 
            smallest_score = heapq.heappop(Wk)
            if total_scores[seq2_obj_id] > smallest_score[0]:
                heapq.heappush(Wk,(total_scores[seq2_obj_id],seq2_obj_id))
            else:
                heapq.heappush(Wk,smallest_score)

        # If the Wk heap exists and the lowest score in the heap is greater than or equal to T, 
        # check if the algorithm can terminate
        if wk_created == 1:
            if Wk[0][0] >= T:
                terminate = True
                # Check if there are any remaining objects that have not been checked yet
                for key in lower_bounds:
                    if key not in objs_seq1:
                        # If the lower bound for the object combined with seq1's score is greater than the Wk threshold, and the object is not in total_scores
                        if Wk[0][0] < round(lower_bounds[key] + seq1_score,2) and key not in total_scores:
                            terminate = False
                            break
                    else:
                        # If the lower bound for the object combined with seq2's score is greater than the Wk threshold, and the object is not in total_scores
                        if Wk[0][0] < round(lower_bounds[key] + seq2_score,2) and key not in total_scores:
                            terminate = False
                            break
                # If no objects meet the criteria above, then terminate the algorithm and record the result
                if terminate == True:
                    print_result(sequential_accesses, Wk)
                    break


def main():
    k = int(sys.argv[1])
    print(k)
    top_k_scores(k)
    
main()
