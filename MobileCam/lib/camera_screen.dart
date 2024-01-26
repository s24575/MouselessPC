import 'package:camera/camera.dart';
import 'package:coolapp/http_server_connection.dart';
import 'package:flutter/material.dart';

class CameraScreen extends StatefulWidget {
  const CameraScreen({
    Key? key,
    required this.cameras,
  }) : super(key: key);

  final List<CameraDescription>? cameras;

  @override
  CameraScreenState createState() => CameraScreenState();
}

class CameraScreenState extends State<CameraScreen> {
  late CameraController _controller;
  bool _isRearCameraSelected = true;

  @override
  void initState() {
    super.initState();
    initCamera(widget.cameras![0]);
  }

  Future<void> initCamera(CameraDescription cameraDescription) async {
    _controller = CameraController(cameraDescription, ResolutionPreset.high);
    try {
      await _controller.initialize().then((_) {
        if (!mounted) return;
        setState(() {});
      });
    } on CameraException catch (e) {
      debugPrint("camera error $e");
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.deepOrange,
        title: const Text('Second Route'),
      ),
      body: Stack(
        children: [
          _controller.value.isInitialized
              ? CameraPreview(_controller)
              : Container(
                  color: Colors.black,
                  child: const Center(child: CircularProgressIndicator()),
                ),
          GestureDetector(
            onTap: () {
              setState(() =>
                  _isRearCameraSelected = !_isRearCameraSelected);
              initCamera(widget.cameras![_isRearCameraSelected ? 0 : 1]);
            },
            child: button(Icons.flip_camera_ios_outlined, Alignment.bottomLeft),
          ),
          GestureDetector(
            onTap: () {
              HttpServerConnection httpServer =
                  HttpServerConnection(_controller);
              httpServer.startServer();
            },
            child: button(Icons.cast, Alignment.bottomRight),
          ),
        ],
      ),
    );
  }

  Widget button(IconData icon, Alignment alignment) {
    return Align(
      alignment: alignment,
      child: Container(
        margin: const EdgeInsets.only(
          left: 20,
          bottom: 20,
        ),
        height: 50,
        width: 50,
        decoration: const BoxDecoration(
          shape: BoxShape.circle,
          color: Colors.white,
          boxShadow: [
            BoxShadow(
              color: Colors.black26,
              offset: Offset(2, 2),
              blurRadius: 10,
            ),
          ],
        ),
        child: Center(
          child: Icon(
            icon,
            color: Colors.black54,
          ),
        ),
      ),
    );
  }
}
