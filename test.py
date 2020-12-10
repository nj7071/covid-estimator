a1 = 0.001   #parameter s katerim okužuje kužni
a2 = 0.00025    #parameter s katerim okužuje bolni
N = 1000   #populacija

cas = 10
D = 999
K = 1
B = 0
O = 0
for dan in range(1, cas):
    novo_okuzeni = round((a1 * K + a2 * B) * D)
    if K + novo_okuzeni < N and D - novo_okuzeni > 0:
        K += novo_okuzeni
        D -= novo_okuzeni
    if K + novo_okuzeni > N and D - novo_okuzeni < 0:
        K = N
        D = 0
    print("kuzni:", K)
    print("dovzetni:", D)
    print("\n")
