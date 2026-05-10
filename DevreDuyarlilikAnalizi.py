import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def main():
    print("Devre Duyarlılık Analizi Başlatılıyor...\n")

    # ==========================================
    # 1. Sembolik Tanımlama (SymPy)
    # ==========================================
    R1, R2, R3, R4 = sp.symbols('R1 R2 R3 R4', real=True, positive=True)
    Ig1, Ig2 = sp.symbols('Ig1 Ig2', real=True)

    # ==========================================
    # 2. Dinamik Matris Oluşturma
    # ==========================================
    # Düğüm gerilimi denklemleri (KCL) baz alınarak Admitans (G) matrisi oluşturulur
    # Düğüm 1: v1*(1/R1 + 1/R2) - v2*(1/R2) = -Ig1
    # Düğüm 2: -v1*(1/R2) + v2*(1/R2 + 1/R3 + 1/R4) = Ig2
    
    G = sp.Matrix([
        [1/R1 + 1/R2, -1/R2],
        [-1/R2, 1/R2 + 1/R3 + 1/R4]
    ])
    I_vector = sp.Matrix([-Ig1, Ig2])

    # Sembolik Çözüm (v = G_inv * I)
    V_vector = G.inv() * I_vector
    v1_sym = V_vector[0]
    v2_sym = V_vector[1]

    # ==========================================
    # 3. Doğrudan Türevleme Modülü
    # ==========================================
    params = [R1, R2, R3, R4, Ig1, Ig2]
    param_names = ['R1', 'R2', 'R3', 'R4', 'Ig1', 'Ig2']
    
    # Her bir parametreye göre kısmi türev alma (dv/dp)
    dv1_dp_sym = [sp.diff(v1_sym, p) for p in params]
    dv2_dp_sym = [sp.diff(v2_sym, p) for p in params]

    # ==========================================
    # 4. Sayısal Dönüşüm (Lambdify)
    # ==========================================
    v1_func = sp.lambdify(params, v1_sym, 'numpy')
    v2_func = sp.lambdify(params, v2_sym, 'numpy')

    dv1_funcs = [sp.lambdify(params, deriv, 'numpy') for deriv in dv1_dp_sym]
    dv2_funcs = [sp.lambdify(params, deriv, 'numpy') for deriv in dv2_dp_sym]

    # ==========================================
    # 5. Sayısal Çözüm & Duyarlılık Sonuçları
    # ==========================================
    # Nominal Değerler
    nominal_vals = (25, 5, 50, 75, 12, 16) # R1, R2, R3, R4, Ig1, Ig2
    
    v1_nom = v1_func(*nominal_vals)
    v2_nom = v2_func(*nominal_vals)

    print("--- NOMİNAL DC ÇÖZÜM ---")
    print(f"v1 = {v1_nom:.3f} V")
    print(f"v2 = {v2_nom:.3f} V\n")

    print("--- SENARYO 1: R1 %10 Artış (27.5 ohm) ---")
    v1_s1 = v1_func(27.5, 5, 50, 75, 12, 16)
    v2_s1 = v2_func(27.5, 5, 50, 75, 12, 16)
    print(f"v1_yeni = {v1_s1:.3f} V")
    print(f"v2_yeni = {v2_s1:.3f} V\n")

    print("--- SENARYO 2: Ig1 13A Yapılması ---")
    v1_s2 = v1_func(25, 5, 50, 75, 13, 16)
    v2_s2 = v2_func(25, 5, 50, 75, 13, 16)
    print(f"v1_yeni = {v1_s2:.3f} V")
    print(f"v2_yeni = {v2_s2:.3f} V\n")

    # Normalize Duyarlılık Katsayılarının Hesaplanması: S_x^y = (x/y) * (dy/dx)
    S_v1 = [(nominal_vals[i] / v1_nom) * dv1_funcs[i](*nominal_vals) for i in range(len(params))]
    S_v2 = [(nominal_vals[i] / v2_nom) * dv2_funcs[i](*nominal_vals) for i in range(len(params))]

    # ==========================================
    # 6. Görselleştirme (Matplotlib)
    # ==========================================
    x = np.arange(len(param_names))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Bar grafikleri oluşturma
    rects1 = ax.bar(x - width/2, S_v1, width, label='$v_1$ Duyarlılığı', color='#944e52')
    rects2 = ax.bar(x + width/2, S_v2, width, label='$v_2$ Duyarlılığı', color='#e8a6a5')

    # Grafik formatlama
    ax.set_ylabel('Normalize Duyarlılık Katsayısı ($S$)', fontsize=12)
    ax.set_title('Parametrelere Göre Düğüm Gerilimi Duyarlılıkları', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(param_names, fontsize=11)
    ax.axhline(0, color='black', linewidth=1) # Sıfır çizgisi
    ax.legend(fontsize=11)
    ax.grid(axis='y', linestyle='--', alpha=0.7)

    # Değerleri barların üzerine yazdırma
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            label_y = height + 0.05 if height > 0 else height - 0.15
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3 if height > 0 else -10), 
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9)
    
    autolabel(rects1)
    autolabel(rects2)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()