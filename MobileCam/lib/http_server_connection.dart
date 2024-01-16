import 'dart:io';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:network_info_plus/network_info_plus.dart';

class HttpServerConnection {
  final CameraController cameraController;
  bool isServerRunning = false;

  HttpServerConnection(this.cameraController);

  void startServer() {
    if (!isServerRunning) {
      _handleHttpConnection();
    }
  }

  void _handleHttpConnection() async {
    final info = NetworkInfo();
    final wifiIP = await info.getWifiIP();

    HttpServer.bind(wifiIP, 4545).then((server) {
      print('Serving at http://${server.address.host}:${server.port}');

      server.listen((HttpRequest request) {
        if (request.uri.pathSegments.isNotEmpty &&
            request.uri.pathSegments.first == 'video') {
          _handleVideoStream(request);
        } else {
          _handleOtherRequests(request);
        }
      });
    });
  }

  void _handleVideoStream(HttpRequest request) {
    request.response.headers.contentType = ContentType('video', 'mp4');

    cameraController.startImageStream((CameraImage image) {
      Uint8List bytes = image.planes[0].bytes;

      request.response.add(bytes);
    });

    request.response.done.whenComplete(() {
      cameraController.stopImageStream();
    });
  }

  void _handleOtherRequests(HttpRequest request) {
    request.response
      ..statusCode = HttpStatus.notFound
      ..write('Not Found')
      ..close();
  }

  // Uint8List _convertImageToBytes(CameraImage image) {
  //   // Implement your logic to convert the CameraImage to bytes
  //   // ...

  //   // Example: Convert the image.planes[0].bytes to Uint8List
  //   final Uint8List bytes = Uint8List.fromList(image.planes[0].bytes);

  //   return bytes;
  // }
}

// Future<String> fetchIpAddress() async {
//   try {
//     var ipAddress = IpAddress(type: RequestType.json);
//     dynamic data = await ipAddress.getIpAddress();
//     return data.toString();
//   } catch (exception) {
//     print(exception.toString());
//     return 'Failed to fetch IP';
//   }
// }
