# Dev Notes


- Android Sim:
-------------
 - Create an image using Android AVD manager (Use UI, Tools to Create AVD/image)
 - This will list existing Images
  - ~/Library/Android/sdk/tools/emulator -list-avds
 - To run this on Android simulator (download/install Android SDK)
 - Pick one of the images (e.g. below)
  - ~/Library/Android/sdk/tools/emulator -avd FourInchAndroid
 - To launch 
  - Point browser to http://10.0.2.2:8080

- iOS Sim:
---------
 - Download (on mac) latest Dev kit
 - Using spotlight (command + space), look for simulator
 - To launch 
  - Point browser to http://localhost:8080

- Cordova Android:
-----------------

- Android sdk is in  (find ~/Library/Android/ -name zipalign)
- Generate key and key store:
 - keytool -genkey -v -keystore dar.ks -alias dar -keyalg RSA -keysize 2048 -validity 10000 (shenba)
- Build
 - cordova build --release android
- Sign
 - jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore dar.ks platforms/android/build/outputs/apk/android-release-unsigned.apk dar 
- Zipalign
 - ~Library/Android//sdk/build-tools/23.0.3/zipalign -v 4 platforms/android/build/outputs/apk/android-release-unsigned.apk platforms/android/build/outputs/apk/Dar.apk
  
