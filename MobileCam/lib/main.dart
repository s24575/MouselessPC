import 'package:camera/camera.dart';
import 'package:coolapp/camera_screen.dart';
import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:network_info_plus/network_info_plus.dart';


Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final cameras = await availableCameras();

  runApp(MaterialApp(home: App(cameras: cameras)));
}

class App extends StatelessWidget {
  final List<CameraDescription> cameras;

  const App({Key? key, required this.cameras}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
        home: Scaffold(
            appBar: appBar(context),
            body: Center(
                child: FutureBuilder<String?>(
              future: fetchIpAddress(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const CircularProgressIndicator();
                } else if (snapshot.hasError) {
                  return Text('Error: ${snapshot.error}');
                } else {
                  return Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      'Connected to IP: ${snapshot.data ?? 'N/A'}',
                      style: const TextStyle(fontSize: 18, color: Colors.white),
                    ),
                    const SizedBox(height: 10),
                    const Text('Port: 4545', style: TextStyle(fontSize: 16, color: Colors.white),
                    ),
                  ],
                );
                }
                }),
                ),
            backgroundColor: Colors.black,
            ));
            
  }

  AppBar appBar(BuildContext context) {
    return AppBar(
      backgroundColor: Colors.black,
      title: const Text("MobileCam"),
      titleTextStyle: const TextStyle(color: Colors.white,  fontSize: 22),
      centerTitle: true,
      actions: [
        GestureDetector(
            onTap: () {
              Navigator.push(
                context,
                MaterialPageRoute(
                    builder: (context) => CameraScreen(cameras: cameras)),
              );
            },
            child: Container(
              margin: const EdgeInsets.all(10),
              alignment: Alignment.center,
              width: 40,
              decoration: BoxDecoration(
                  color: Colors.black,
                  borderRadius: BorderRadius.circular(10)),
              child: SvgPicture.asset(
                'assets/icons/camera_icon.svg',
                height: 30,
                width: 30,
                color: Colors.white,
              ),
            ))
      ],
    );

  }

  Future<String?> fetchIpAddress() async {
    final info = NetworkInfo();
    final wifiIP = await info.getWifiIP();
    return wifiIP;
  }
}
