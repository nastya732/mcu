import time
import serial
import matplotlib.pyplot as plt
import numpy as np

def read_value(ser, timeout=2.0):
    """Читает одно значение от устройства с таймаутом"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('ascii').strip()
                if line:
                    return float(line)
        except (ValueError, UnicodeDecodeError):
            continue
        time.sleep(0.01)
    return None

def main():
    print("=== BME280 Data Logger ===")
    print("Сбор 100 измерений...")
    
    ser = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=1.0)
    
    if ser.is_open:
        print(f"Port {ser.name} opened")
    else:
        print(f"Port {ser.name} closed")
        return
    
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    C = []
    P = []
    H = []
    ts = []
    
    start_ts = time.time()
    
    print("\nНачинаем сбор данных...\n")
    
    try:
        for i in range(100):
            ser.write(b"temp\n")
            time.sleep(0.05)
            temp_C = read_value(ser)
            if temp_C is None:
                continue
            
            ser.write(b"pres\n")
            time.sleep(0.05)
            pres_P = read_value(ser)
            if pres_P is None:
                continue
            
            ser.write(b"hum\n")
            time.sleep(0.05)
            hum_H = read_value(ser)
            if hum_H is None:
                continue
            
            current_time = time.time() - start_ts
            ts.append(current_time)
            C.append(temp_C)
            P.append(pres_P)
            H.append(hum_H)
            
            print(f"[{current_time:.1f}s] {i+1:3d}: T={temp_C:.2f}°C, P={pres_P:.0f}Pa, H={hum_H:.1f}%")
            time.sleep(0.2)
            
    except KeyboardInterrupt:
        print("\n\nПрервано пользователем")
    
    finally:
        ser.close()
        print("\nPort closed")
        
        if len(ts) == 0:
            print("Нет данных для построения графиков")
            return
        
        times = np.array(ts)
        temps = np.array(C)
        pressures = np.array(P)
        hums = np.array(H)
        
        # Создаем три графика
        fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
        
        # График температуры
        ax1.plot(times, temps, 'r-', linewidth=2)
        ax1.set_ylabel('Температура (°C)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        
        # График давления
        ax2.plot(times, pressures, 'b-', linewidth=2)
        ax2.set_ylabel('Давление (Па)', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        # График влажности
        ax3.plot(times, hums, 'g-', linewidth=2)
        ax3.set_xlabel('Время (с)', fontsize=12)
        ax3.set_ylabel('Влажность (%)', fontsize=12)
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    main()