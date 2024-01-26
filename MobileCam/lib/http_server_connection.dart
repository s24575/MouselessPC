import 'dart:io';
import 'dart:typed_data';
import 'package:camera/camera.dart';
import 'package:network_info_plus/network_info_plus.dart';
import 'dart:convert';
import 'package:image/image.dart' as img;

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

  void _handleVideoStream(HttpRequest request) async{
    // request.response.headers.contentType = ContentType('video', 'mp4');
    request.response.headers.contentType = ContentType('image', 'jpeg');

    // cameraController.startImageStream((CameraImage cameraImage) {
    //   // Uint8List bytes = image.planes[0].bytes;
    //     print(cameraImage.format);
    //     print("Camera width:  ${cameraImage.width} ");
    //     print("Camera height:  ${cameraImage.height} ");
    //   img.Image image = img.Image.fromBytes(
    //       width: cameraImage.width,
    //       height: cameraImage.height,
    //       bytes: cameraImage.planes[0].bytes.buffer);
    //   // Uint8List list = Uint8List.fromList(img.encodeJpg(image));
    //   img.Image resizedImage = img.copyResize(image, width: 640, height: 480);

    //   // request.response.write(list);
    //   Uint8List jpegBytes = Uint8List.fromList(img.encodeJpg(resizedImage));
    //   String base64Image = base64Encode(jpegBytes);

    //   // Send the image tag in the response
    //   String dataUrl = 'data:image/jpeg;base64, $base64Image';
    //   request.response.write('<img src="$dataUrl" />');
    // });

    // request.response.done.whenComplete(() {
    //   cameraController.stopImageStream();
    // });

    final image = await cameraController.takePicture();
    request.response.write(image);
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