Görev Zamanlayıcı ile Ayda 1 Kez Çalışacak PowerShell Scripti Kurulumu

1. **Başlat Menüsü > Görev Zamanlayıcı (Task Scheduler) yaz ve aç.**

2. **Görev Zamanlayıcı Açıldığında:**
   - Sağ tarafta **"Görev Oluştur (Create Task...)"** seçeneğine tıklayın.

3. **Genel (General) Sekmesinde:**
   - Göreve bir isim ver, örneğin: **"Aylık Backup Script"**
   - **"Yalnızca kullanıcı oturum açtığında çalıştır"** veya **"Kullanıcı oturum açmasa bile çalıştır"** seçeneğini seçin.

4. **Tetikleyiciler (Triggers) Sekmesinden:**
   - **"Yeni (New...)"** butonuna tıklayın.
   - **"Aylık (Monthly)"** seçeneğini işaretleyin.
   - **Aylar:** Tüm aylar işaretli olmalı (Ocak, Şubat, ... Aralık).
   - **Günler:** Sadece **1**'i seçin (ya da istediğiniz başka bir gün).
   - Bu ayar, **her ayın 1'inde** çalıştıracaktır.

5. **Eylemler (Actions) Sekmesinden:**
   - **"Yeni (New...)"** butonuna tıklayın.
   - **Eylem** kısmında **"Program başlat (Start a program)"** seçili olmalı.
   
6. **Program/Script:**
   - Program yolunu **"powershell.exe"** olarak yazın:
     ```
     C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe
     ```

7. **Bağımsız Değişkenler (Arguments) Kısmına Şunları Yazın:**

8. **Ayarları Kaydedin ve Çıkın.**

Not: `C:\Scripts\backup.ps1` yolunu kendi script dosyanızın yolu ile değiştirin.

---

**Görev Zamanlayıcı Üzerinden Görevi Elle Tetikleme**

1. **Görev Zamanlayıcı'yı Aç:**
- Başlat menüsüne **"Görev Zamanlayıcı"** yazın ve açın.

2. **Görevi Bul:**
- Sol panelde, **"Görev Zamanlayıcı Kitaplığı"** (Task Scheduler Library) 'na tıklayın. Ortadaki panelden **"Aylık Backup Script"** gibi görev ismini bulun. Eğer görevi bir klasöre kaydettiyseniz, o klasöre gidin.

3. **Görevi Seçin:**
- Sağ panelde, oluşturduğunuz görevi (örneğin **"Aylık Backup Script"**) bulun ve sağ tıklayın.

4. **Görevi Tetikleyin:**
- Sağ tıklama menüsünde, **"Şimdi Çalıştır"** (Run) seçeneğini tıklayın.
- Görev hemen çalışacaktır ve scriptiniz tetiklenir.

---

Bu talimatlarla, hem Görev Zamanlayıcı üzerinden zamanlanmış görevi kurabilir hem de elle tetikleyebilirsiniz. 

Not: `C:\Scripts\backup.ps1` yolunu kendi script dosyanızın yolu ile değiştirmeyi unutmayın.