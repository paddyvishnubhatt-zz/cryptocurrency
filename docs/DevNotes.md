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

- Cordova iOS:
-------------
 - Build the app
  - App ID
  - Certs
  - Mobile provisioning certs
 - cordova build --release ios
 - XCode
  - Test by running from XCode w/ one of the devices
  - Archive
  - Upload ipa to iTunes/App store
  - Test Flight
   - Add internal tester(s)
   - Add App (select version)
   - Have tester install test-flight app and then the app and start testing
  
- Cordova Android:
-----------------

 - Android sdk is in  (find ~/Library/Android/ -name zipalign)
 - Generate key and key store:
 - keytool -genkey -v -keystore crypto.ks -alias crypto -keyalg RSA -keysize 2048 -validity 10000 (shenba)
 - Build
  - cordova build --release android
 - Sign
  - jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore crypto.ks platforms/android/build/outputs/apk/android-release-unsigned.apk crypto 
 - Zipalign
  - ~/Library/Android//sdk/build-tools/23.0.3/zipalign -v 4 platforms/android/build/outputs/apk/android-release-unsigned.apk platforms/android/build/outputs/apk/rypto.apk
 - Publish
  - Publish using google/play-store console
  
- GAE:
-----
1. Get google account
2. Create a project
3. Login into google cloud from command line (this will prompt browser login/oauth): 
 - gcloud auth login
4. Deploy app using:
 - gcloud app deploy app.yaml index.yaml cron.yaml --project cryptocurrency-1003
5. gcloud app browser --project ...

  
- DNS:
-----
2. When asked to verify w/ iPage, use CNAME
3. Get the CNAME records from the GAE utility and plunk them in iPAGE CNAME records
4. Good to go

