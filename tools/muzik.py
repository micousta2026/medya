#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Micousta Instagram videolari icin ozgun, enerjik muzik uretir.
Kullanim: python3 muzik.py <cikis.wav> <saniye> <seed>
Her seed farkli tonalite, tempo, progresyon ve dokulu bir parca verir."""
import sys, wave
import numpy as np

SR = 44100

def synth(dur, seed=0):
    rng = np.random.default_rng(seed)
    bpm   = int(rng.integers(102, 133))
    spb   = 60.0 / bpm
    roots = [55.00, 58.27, 61.74, 65.41, 69.30, 73.42, 77.78, 82.41]
    root  = roots[int(rng.integers(0, len(roots)))]
    minor = bool(rng.random() < 0.62)
    n = int(SR * dur); t = np.arange(n) / SR
    out = np.zeros(n)

    sc = [0,3,5,7,10] if minor else [0,2,4,7,9]
    pool = [0,0,3,5,7,8,10] if minor else [0,0,4,5,7,9]
    prog = [pool[int(rng.integers(0,len(pool)))] for _ in range(4)]
    def hz(semi, oct_=0): return root * 2**(semi/12 + oct_)

    bar = spb*4
    nb  = int(np.ceil(dur/bar))

    def place(buf, start, sig, gain=1.0):
        i = int(start*SR)
        if i >= n: return
        L = min(len(sig), n-i)
        buf[i:i+L] += sig[:L]*gain

    # --- davul ---
    def kick():
        L=int(0.26*SR); x=np.arange(L)/SR
        f=np.exp(-x*34)*92+46
        s=np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-x*9.0)
        s+=np.exp(-x*210)*0.5*rng.normal(0,1,L)
        return s*0.92
    def hat(open_=False):
        L=int((0.12 if open_ else 0.045)*SR); x=np.arange(L)/SR
        s=rng.normal(0,1,L)
        s=s-np.convolve(s,np.ones(9)/9,mode='same')          # yuksek gecis
        return s*np.exp(-x*(16 if open_ else 55))*0.17
    def clap():
        L=int(0.21*SR); x=np.arange(L)/SR
        s=rng.normal(0,1,L); s=s-np.convolve(s,np.ones(26)/26,mode='same')
        env=np.exp(-x*13)*(1-np.exp(-x*140))
        return s*env*0.40

    for b in range(nb*4):
        beat=b*spb
        if beat>dur: break
        place(out, beat, kick(), 1.0 if b%4!=3 else 0.9)
        if b%4 in (1,3): place(out, beat, clap())
        for h in range(2):
            place(out, beat+h*spb/2, hat(open_=(b%4==3 and h==1)), 1.0 if h==0 else 0.75)

    # --- bas ---
    for b in range(nb*4):
        beat=b*spb
        if beat>dur: break
        semi=prog[(b//4)%4]
        f=hz(semi)
        L=int(spb*0.92*SR); x=np.arange(L)/SR
        saw=2*((f*x)%1)-1
        sub=np.sin(2*np.pi*f*x)
        env=(1-np.exp(-x*220))*np.exp(-x*3.4)
        place(out, beat, (0.55*saw+0.75*sub)*env*0.30)

    # --- arp (16'lik) ---
    step=spb/4
    k=0
    while k*step < dur:
        semi=prog[(int(k*step/bar))%4]
        deg=sc[(k + (k//4)) % len(sc)]
        f=hz(semi+deg, 2 if (k%8)<4 else 3)
        L=int(step*1.6*SR); x=np.arange(L)/SR
        sq=np.sign(np.sin(2*np.pi*f*x))*0.45 + np.sin(2*np.pi*f*x)*0.55
        env=(1-np.exp(-x*300))*np.exp(-x*11.0)
        swell=0.55+0.45*np.sin(2*np.pi*(k*step)/max(dur,1)*2.0)
        place(out, k*step, sq*env*0.115*swell)
        k+=1

    # --- pad ---
    pad=np.zeros(n)
    for b in range(nb):
        semi=prog[b%4]; start=b*bar
        L=int(min(bar, dur-start)*SR)
        if L<=0: break
        x=np.arange(L)/SR
        ch=[0,3,7,10] if minor else [0,4,7,11]
        s=np.zeros(L)
        for c in ch:
            f=hz(semi+c,1)
            s+=np.sin(2*np.pi*f*x)+0.5*np.sin(2*np.pi*f*1.004*x)
        s/=len(ch)*1.5
        env=(1-np.exp(-x*5))*np.exp(-x*0.5)
        place(pad, start, s*env)
    out += pad*0.22

    # --- riser (son boluma giris) ---
    if dur > 8:
        rs=int((dur*0.62)*SR); L=int(min(2.0,dur*0.2)*SR)
        x=np.arange(L)/SR
        nz=rng.normal(0,1,L); nz=nz-np.convolve(nz,np.ones(7)/7,mode='same')
        out[rs:rs+L]+= nz*np.linspace(0,1,L)**2.2*0.14

    # --- bitis ---
    fi=int(0.08*SR); fo=int(min(1.8,dur*0.12)*SR)
    out[:fi]*=np.linspace(0,1,fi); out[-fo:]*=np.linspace(1,0,fo)

    # yumusak limit
    out=np.tanh(out*1.25)
    out/=np.max(np.abs(out))*1.02
    wide=np.stack([out, np.roll(out,140)],axis=1)
    return wide, bpm, root, minor

def main():
    path=sys.argv[1]; dur=float(sys.argv[2]); seed=int(sys.argv[3])
    st,bpm,root,minor=synth(dur,seed)
    pcm=(st*32767*0.90).astype(np.int16)
    with wave.open(path,"wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    print(f"{path}  {dur:.1f}s  {bpm} BPM  {'minor' if minor else 'major'}  seed={seed}")

if __name__=="__main__":
    main()
