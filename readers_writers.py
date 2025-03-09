import threading
import time
import random

# -----------------------------------------------------------------------------
# Global Shared Variables and Synchronization Primitives
# -----------------------------------------------------------------------------

# create a lock to protect shared state from concurrent access
lock = threading.Lock()
condition = threading.Condition(lock)
# tracks how many readers are accessing each replica (index 0 to 2)
read_counts = [0, 0, 0]
writer_active = False      # True when writer is updating
writer_waiting = False     # True when writer is waiting to update

# simulated content for three file replicas
file_contents = [
    "Initial content of replica 1",
    "Initial content of replica 2",
    "Initial content of replica 3"
]

# lock for logging so that log writes don’t interleave
log_lock = threading.Lock()


# -----------------------------------------------------------------------------
# Logging function
# -----------------------------------------------------------------------------

def log_event(actor, replica_index, operation, content):
    
    #Logs the details of read or write operations to a log file "log.txt"
    #actor (str): identifier for the thread (for instance, "Reader" or "Writer")
    #replica_index (int or None): the index of the replica accessed (None for writer)
    #operation (str): type of operation ("read" or "write")
    #content (str): the content read from or written to the replica/replicas

    with log_lock:
        with open("log.txt", "a") as log_file:
            timestamp = time.ctime()
            
            # build log message with current state snapshot
            log_message = f"[{timestamp}] Operation: {operation.upper()}, Actor: {actor}, "
            if operation == "read":
                log_message += f"Replica: {replica_index + 1}, Content: '{content}', "
            else:
                log_message += f"Updated all replicas with: '{content}', "
            log_message += f"Read counts: {read_counts}, Writer active: {writer_active}\n"
            log_file.write(log_message)

            # optionally, also print the log message to console
            print(log_message, end="")

# -----------------------------------------------------------------------------
# Reader function
# -----------------------------------------------------------------------------

def reader(reader_id):
    global writer_active, writer_waiting, read_counts
    with condition:

        # if a writer is active or waiting, the reader must wait
        while writer_active or writer_waiting:
            condition.wait()

        # choose the replica with the minimum number of readers for load balancing
        replica_index = read_counts.index(min(read_counts))
        read_counts[replica_index] += 1

    # simulate reading (release the lock while reading)
    time.sleep(random.uniform(0.1, 0.5))  # simulate variable read time
    content = file_contents[replica_index]

    # log the read event
    log_event(f"Reader-{reader_id}", replica_index, "read", content)

    with condition:
        read_counts[replica_index] -= 1

        # notify waiting threads (possibly the writer waiting for all readers to finish)
        condition.notify_all()

# -----------------------------------------------------------------------------
# Writer function
# -----------------------------------------------------------------------------

def writer():
    global writer_active, writer_waiting, file_contents
    while True:

        # sleep for a random duration before attempting a write
        time.sleep(random.uniform(1, 3))
        with condition:

            # indicate that a writer is waiting so that new readers wait
            writer_waiting = True

            # wait until all readers have finished
            while any(count > 0 for count in read_counts):
                condition.wait()

            # mark that the writer is active.
            writer_active = True
            writer_waiting = False

        # writer has exclusive access here
        new_content = f"Updated at {time.ctime()}"

        # update all file replicas simultaneously
        for i in range(len(file_contents)):
            file_contents[i] = new_content

        # log the write event
        log_event("Writer", None, "write", new_content)

        with condition:
            writer_active = False

            # notify all waiting threads (both readers and a potential writer)
            condition.notify_all()

# -----------------------------------------------------------------------------
# Main function
# -----------------------------------------------------------------------------

def main():

    # start the writer thread
    writer_thread = threading.Thread(target=writer, daemon=True)
    writer_thread.start()

    reader_id = 1
    try:
        # continuously spawn reader threads at random intervals
        while True:
            time.sleep(random.uniform(0.2, 1))
            t = threading.Thread(target=reader, args=(reader_id,), daemon=True)
            t.start()
            reader_id += 1
    except KeyboardInterrupt:
        print("Shutting down simulation.")

if __name__ == "__main__":
    main()
