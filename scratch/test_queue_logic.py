import random

class QueueManager:
    def __init__(self, track_count=5):
        self.songs = list(range(track_count))
        self.queue = list(range(len(self.songs)))
        self.user_ordered_queue = self.queue.copy()
        self.queue_index = 0
        self.shuffle_enabled = False
        self.repeat_mode = "off" # "off", "all", "one"

    def toggle_shuffle(self):
        self.shuffle_enabled = not self.shuffle_enabled
        if self.shuffle_enabled:
            current = self.queue[self.queue_index]
            rest = self.user_ordered_queue.copy()
            if current in rest: rest.remove(current)
            random.shuffle(rest)
            self.queue = [current] + rest
            self.queue_index = 0
        else:
            current_song = self.queue[self.queue_index]
            self.queue = self.user_ordered_queue.copy()
            self.queue_index = self.queue.index(current_song)

    def next_song(self):
        if not self.queue: return None
        if self.repeat_mode == "one":
            return self.queue[self.queue_index]
        self.queue_index += 1
        if self.queue_index >= len(self.queue):
            if self.repeat_mode == "all":
                self.queue_index = 0
            else:
                self.queue_index = len(self.queue) - 1
                return None
        return self.queue[self.queue_index]

    def prev_song(self):
        if not self.queue: return None
        self.queue_index -= 1
        if self.queue_index < 0:
            self.queue_index = (len(self.queue) - 1) if self.repeat_mode == "all" else 0
        return self.queue[self.queue_index]

def test_queue():
    qm = QueueManager(track_count=5)
    assert qm.queue == [0, 1, 2, 3, 4]
    
    # Advance to track 2
    qm.next_song() # 1
    t = qm.next_song() # 2
    assert t == 2
    assert qm.queue_index == 2
    
    # Toggle shuffle: track 2 must stay at index 0, others shuffled
    qm.toggle_shuffle()
    assert qm.shuffle_enabled is True
    assert qm.queue[0] == 2
    assert sorted(qm.queue) == [0, 1, 2, 3, 4]
    assert len(qm.queue) == 5
    
    # Toggle unshuffle: original order restored, active track remains track 2 at index 2
    qm.toggle_shuffle()
    assert qm.shuffle_enabled is False
    assert qm.queue == [0, 1, 2, 3, 4]
    assert qm.queue_index == 2
    
    # Test repeat "all"
    qm.repeat_mode = "all"
    qm.queue_index = 4
    next_t = qm.next_song()
    assert next_t == 0, "Repeat all should loop to index 0!"
    
    # Test repeat "one"
    qm.repeat_mode = "one"
    for _ in range(5):
        assert qm.next_song() == 0, "Repeat one must stay on track 0!"
        
    print("Queue manager shuffle/repeat logic test passed successfully!")

if __name__ == "__main__":
    test_queue()
