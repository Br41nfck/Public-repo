Настройка PXE на Linux Debian

### Установка Linux Debian ###
1) Устанавливаем образ Linux Debian 12.10 (Graphical Install)
2) Местонахождение - любое
3) Настройка клавиатуры - English
4) Имя компьютера - <NETBIOS>
5) Имя домена - <COMPANYNAME>
6) Пароль суперпользователя (root) - указываем самостоятельно
7) Имя пользователя (<user>) - указываем самостоятельно
8) Пароль пользователя (<user>) - указываем самостоятельно
9) Настройка часовых поясов - ставим GPT +3 (Россия, Москва, Санкт-Петербург)
10) Настройка разметки диска - указываем "разбить на разделы"
11) Записать изменения на диск? - указываем "Да"
12) Использовать установочный носитель? - указываем "Нет"
13) Использовать зеркало архива из сети? - указываем "Да"
14) Указываем "Российская федерация"
15) Выбираем зеркало "deb.debian.org"
16) Использовать прокси? - указываем "нет"
17) Участвовать в сборе статистики? - указываем "Нет"
18) Устанавливаем окружение Xfce, SSH-сервер, дополнительные утилиты
19) Жмём "Готово"

20) После установки заходим под суперпользователем (root), добавляем пользователя user в список sudoers (для установки и настройки пакетов из SSH)
su root
nano /etc/sudoers
Ищем строку "#User privilege specification", после строки "root ALL=(ALL)	ALL" добавляем "<user> ALL=(ALL)	ALL"


#### Полезности ####
sudo apt install fish # Подсветка синтаксиса и автодополнение по Tab
sudo apt install tmux # Мультисессионный терминал
sudo apt install tree # Вывод файлов и папок в виде дерева
sudo apt install net-tools # для работы ifconfig
sudo apt install vim  # Текстовый редактор
sudo apt install pmount # Работа с флешками
pmount /dev/sd[b-z]N - смонтировать накопитель
umount /dev/sd[b-z]N - размонтировать накопитель
cd /media/_sd[b-z]N
sudo apt install mc # Файловый менеджер
sudo apt install rsync # Копирование с прогресс-баром
rsync -ah --progress SOURCE DESTINATION
alias ls="ls -al" # при команде ls вывод всех файлов (включая скрытые) в виде списка 


21) Задаём статический адрес для сервера:
P.S. Перед этим делаем бекап: cp /etc/network/interfaces /etc/network/interfaces_backup
sudo vim /etc/network/interfaces
Указываем:
allow-hotplug enp0s31f6 				# Автоматически перезапускать интерфейс при падении (enp0s31f6 - сетевой интерфейс подключения)
auto enp0s31f6 							# Автоматически поднимать интерфейс при загрузке системы
iface enp0s31f6 inet static 			# Задать статический IP-адрес
address 192.168.XX.XX 					# IP-адрес
netmask 255.255.XX.XX 					# Маска сети
gateway 192.168.XX.XX					# Шлюз 
dns-nameservers 192.168.XX.XX 8.8.8.8 	# DNS-сервера

22) обновляем пакеты и устанавливаем последние обновления:
apt update && apt upgrade

23) Заходим под пользователем, проверяем права:
sudo apt update

P.S. Тут уже можно коннектиться по SSH (для коннекта на Windows можно использовать PuTTY

24) Так как будем грузиться через HTTP, создадим папку "images" в /var/www/html, где будут храниться образы:
sudo mkdir -p /var/www/html/images

25) Настройка DHCP сервера. Наш PXE-сервер будет раздавать IP-адреса клиентам нашей сети при подключении к нему.
Устанавливаем пакет для настройки DHCP-сервера:
sudo apt install isc-dhcp-server

26) Назначаем интерфейс для прослушивания:
sudo vim /etc/default/isc-dhcp-server
Указываем:
INTERFACESv4="ETH0"

27) Указать файл конфигурации!!!

28) Проверка настроек dhcp сервера на ошибки: dhcpd -t -cf /etc/dhcd/dhcpd.conf
29) Рестарт DHCP-сервера: systemctl restart isc-dhcp-server

TL;DR https://www.iana.org/assignments/bootp-dhcp-parameters/bootp-dhcp-parameters.xhtml - Список кодов DHCP сервера
## Standard ISC dhcpd options specific to iPXE 
  option space ipxe;
  option ipxe-encap-opts code 175 = encapsulate ipxe;
  option ipxe.priority code 1 = signed integer 8;
  option ipxe.keep-san code 8 = unsigned integer 8;
  option ipxe.skip-san-boot code 9 = unsigned integer 8;
  option ipxe.syslogs code 85 = string;
  option ipxe.cert code 91 = string;
  option ipxe.privkey code 92 = string;
  option ipxe.crosscert code 93 = string;
  option ipxe.no-pxedhcp code 176 = unsigned integer 8;
  option ipxe.bus-id code 177 = string;
  option ipxe.san-filename code 188 = string;
  option ipxe.bios-drive code 189 = unsigned integer 8;
  option ipxe.username code 190 = string;
  option ipxe.password code 191 = string;
  option ipxe.reverse-username code 192 = string;
  option ipxe.reverse-password code 193 = string;
  option ipxe.version code 235 = string;
  option iscsi-initiator-iqn code 203 = string;
  option ipxe.pxeext code 16 = unsigned integer 8;
  option ipxe.iscsi code 17 = unsigned integer 8;
  option ipxe.aoe code 18 = unsigned integer 8;
  option ipxe.http code 19 = unsigned integer 8;
  option ipxe.https code 20 = unsigned integer 8;
  option ipxe.tftp code 21 = unsigned integer 8;
  option ipxe.ftp code 22 = unsigned integer 8;
  option ipxe.dns code 23 = unsigned integer 8;
  option ipxe.bzimage code 24 = unsigned integer 8;
  option ipxe.multiboot code 25 = unsigned integer 8;
  option ipxe.slam code 26 = unsigned integer 8;
  option ipxe.srp code 27 = unsigned integer 8;
  option ipxe.nbi code 32 = unsigned integer 8;
  option ipxe.pxe code 33 = unsigned integer 8;
  option ipxe.elf code 34 = unsigned integer 8;
  option ipxe.comboot code 35 = unsigned integer 8;
  option ipxe.efi code 36 = unsigned integer 8;
  option ipxe.fcoe code 37 = unsigned integer 8;
  option ipxe.vlan code 38 = unsigned integer 8;
  option ipxe.menu code 39 = unsigned integer 8;
  option ipxe.sdi code 40 = unsigned integer 8;
  option ipxe.nfs code 41 = unsigned integer 8;

30) Клонируем ipxe
git clone https://github.com/ipxe/ipxe.git
cd ipxe/src

# Включаем поддержку NFS
sed -i 's/#undef\tDOWNLOAD_PROTO_NFS/#define\tDOWNLOAD_PROTO_NFS/' config/general.h

# Включаем команду ping 
sed -i 's/\/\/#define\ PING_CMD/#define\ PING_CMD/' config/general.h
sed -i 's/\/\/#define\ IPSTAT_CMD/#define\ IPSTAT_CMD/' config/general.h
sed -i 's/\/\/#define\ REBOOT_CMD/#define\ REBOOT_CMD/' config/general.h
sed -i 's/\/\/#define\ POWEROFF/#define\ POWEROFF/' config/general.h

# Также включить поддержку команд консоли  
>sudo vim config/console.h 
Убираем один '#' с "##define CONSOLE_FRAMEBUFFER"

>sudo vim config/general.h 
Убираем один '#' с "##define CONSOLE_CMD"

31) Создаём скрипт настройки, он должен лежать в папке "ipxe/src"
>vim start.ipxe

#!ipxe

dhcp
chain tftp://${next-server}/main.ipxe || shell

32) Собираем загрузчики по очереди
make bin-i386-efi/ipxe.efi EMBED=start.ipxe
make bin-i386-pcbios/undionly.kpxe EMBED=start.ipxe	

Если всё хорошо, на выходе получаем сообщения: 
[FINISH] bin-i386-efi/ipxe.efi - после компиляции ipxe.efi 
[FINISH] bin-i386-pcbios/undionly.kpxe - после компиляции undionly.kpxe

33) Копируем загрузчики на PXE-сервер
cp bin-i386-efi/ipxe.efi /srv/tftp/
cp bin-i386-efi/undionly.efi /srv/tftp/

34) Пишем boot-скрипт
>sudo vim /srv/tftp/boot.ipxe

#!ipxe
set httpServer http://<IP-ADDRESS>:80 # Устанавливаем адрес нашего PXE-сервера
set menu-timeout 10000 # Тайм-аут выхода из загрузки
# Также можно загрузить фоновое изображение PXE-Сервера
# Картинки должны иметь название и расширение pcbios.png и efi.png, формат 1024x768 и лежать в папке /var/www/html/images/photo/
# console -l 32 -r 32 -t 32 -b 32 -k --x 1024 --y 768 -d 24 -p ${httpServer}/images/photo/${platform}.png # platform - отвечает за режим загрузки (bios или uefi)
imgfree ${platform}.png # Удаляем картинку из памяти
: login
login || goto cancel

:next
chain --replace --autofree menu.ipxe

35) Пишем меню загрузки ОС
>vim 

#!ipxe
# Цвет по-умолчанию (индекс 0)
# Буквы - черный, фон-прозрачный
cpair -f 0 -b 4 0

# Нормальный текст (индекс 1)
# Буквы - черный, фон - прозрачный
cpair -f 0 -b 4 1

# Разделители (индекс 3)
# Буквы - красный, фон - прозрачный
cpair -f 1 -b 4 3

#########################

######## Главное меню ########
# На данный момент "всё в одном", но можно разделить как по разным меню, так и по разным файлам
:start
# Составляю меню
# https://ipxe.org/cmd/menu
menu iPXE boot menu
item -k e exit (E)xit and boot from disk
item
item --gap -- -------- Windows Images --------
item -k a win10manager2021 Windows 10 M(a)nager 2021
item
item --gap -- -------- Debian Images --------
item debian11 Debian 11 Bullseye
item --gap -- -------- iPXE Utilites --------
item -k c config Start interactive (c)onfiguration tool
item -k s shell Start (S)hell iPXE

choose -d exit -t ${menu-timeout} selected
goto ${selected}

########
# Пункты меню
# В среднем состоят из трёх пунктов:
# kernel - передаю ядро linux и аргументы для запуска
# initrd - пакет данных для ядра
# boot - команда передачи управления ядру linux

########
:debian11
# В данном случае, в kernel передаётся ссылка linux ядра на http-сервере и аргументы запуска
kernel ${httpServer}/images/bullseye/install.amd/linux auto=true priority=high vga=788 url=${httpServer}/images/bullseye_2/install.amd/pxe_general_${platform}_preseed.cfg netcfg/dhcp_failed=note netcfg/dhcp_options="Retry network autoconfiguration" netcfg/get_domain=  --- quiet initrd=initrd.gz

# так же, ссылкой на http, передается пакет данных для ядра
initrd ${httpServer}/images/bullseye/install.amd/initrd.gz

# команда передачи управления ядру linux и в случае ошибки - переход к обоку обработки ошибок
boot || goto error
goto start

# Разбор файлов для linux
:win10manager2021
# wimboot - загрузчик .wim файлов установщика Windows, который сам патчит BCD, запускает установку и подтягивает скрипты запуска
# https://ipxe.org/wimboot
kernel wimboot
###########################################
# Неизменный блок для любого образа Windows
###########################################
initrd ${httpServer}/images/winpe/Boot/BCD BCD           # Стандартный BCD WinPE
initrd ${httpServer}/images/winpe/Boot/boot.sdi boot.sdi # Стандартный boot.sdi WinPE
initrd ${httpServer}/images/winpe/boot.wim boot.wim      # Стандартный boot.wim
initrd configWPE/winpeshl.ini winpeshl.ini               # Конфиг запускающий скрипт установки.
###########################################

# Изменяемые данные в зависимости от образа
initrd configWPE/win10manager2021/install.bat install.bat   # Скрипт установки образа
boot || goto error

goto start
# При ошибках выход на командную строку
:error
echo Failed - have error
sleep 1
goto shell
##############################

35) Создаю папки для хранения загрузчика и файлов ответа
mkdir -p /var/www/html/images/linux/debian11/install.amd # Для загрузчика, файлов ответа
mkdir -p /var/www/html/images/linux/debian11/postinstall # Для скриптов и пакетов пост-установки. Скачиваться будут благодаря команде в файле ответов
cd /var/www/html/images/linux/debian11/install.amd/

# Загрузка ядра 
wget http://ftp.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/debian-installer/amd64/linux
# Пакет данных
wget http://ftp.debian.org/debian/dists/stable/main/installer-amd64/current/images/netboot/debian-installer/amd64/initrd.gz

# Загрузка драйверов в ядро (выполнять под суперпользователем: sudo -i)
[ -f initrd.gz.orig ] || cp -p initrd.gz initrd.gz.orig
[ -f firmware.cpio.gz ] || wget http://cdimage.debian.org/cdimage/unofficial/non-free/firmware/stable/current/firmware.cpio.gz
cat initrd.gz.orig firmware.cpio.gz > initrd.gz

36) Создаю файл ответов для debian в папке /var/www/html/images/linux/debian11/install.amd
pxe_efi_preseed.cfg с разметкой диска под UEFI
pxe_pcbios_preseed.cfg с разметкой диска под Legacy

########### Windows #########
37) Скачиваем wimboot (https://github.com/ipxe/wimboot/releases/download/v2.8.0/wimboot)
wget https://github.com/ipxe/wimboot/releases/download/v2.8.0/wimboot
(git clone https://github.com/ipxe/wimboot.git) 

Распаковываем wimboot в srv/tftp/: 
>cp wimboot /srv/tftp/

Структура файлов для загрузки по iPXE должна быть такая:
ipxe.efi
menu.ipxe
undionly.kpxe
wimboot    

Продолжение следует...
