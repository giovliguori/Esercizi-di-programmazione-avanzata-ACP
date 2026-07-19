from MagazzinoImpl import MagazzinoImpl

IP = "localhost"
PORT = 0
QUEUE_SIZE = 5

# Creo una istanza del servizio reale, dato che lo Skeleton è per ereditarietà
# ed avvio lo skeleton
magazzino = MagazzinoImpl(IP, PORT, QUEUE_SIZE)
magazzino.runSkeleton()

print("[MAGAZZINO SERVER] Started")