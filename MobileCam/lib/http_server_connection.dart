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
      // print('Serving at http://${server.address.host}:${server.port}');

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
    request.response.headers.contentType = ContentType('multipart', 'x-mixed-replace', parameters: {'boundary': 'myboundary'});


    cameraController.startImageStream((CameraImage cameraImage) {

      img.Image image = img.Image.fromBytes(
          width: cameraImage.width,
          height: cameraImage.height,
          bytes: cameraImage.planes[0].bytes.buffer);
      
      img.Image resizedImage = img.copyResize(image, width: 640, height: 480);

      Uint8List jpegBytes = Uint8List.fromList(img.encodeJpg(resizedImage));
      // String base64Image = base64Encode(jpegBytes);

      // String dataUrl = 'data:image/jpeg;base64, $base64Image';
      // request.response.write('<img src="$dataUrl" />');

      String boundary = 'myboundary';
      request.response.write('--$boundary\r\n');
      request.response.write('Content-Type: image/jpeg\r\n');
      request.response.write('Content-Length: ${jpegBytes.length}\r\n\r\n');
      request.response.add(jpegBytes);
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
}
