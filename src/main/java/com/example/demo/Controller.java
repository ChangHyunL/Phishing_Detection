package com.example.demo;

import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.awt.*;
import java.io.File;

@org.springframework.stereotype.Controller
@RequiredArgsConstructor
public class Controller {
    @GetMapping("/scan")
    public String scan(){
        return "QRcodeScanner";
    }

    @PostMapping("/scan")
    public ResponseEntity<String> handleFileUpload(@RequestParam("image") MultipartFile file) {
        if (file.isEmpty()) {
            return new ResponseEntity<>("이미지를 선택해주세요.", HttpStatus.BAD_REQUEST);
        }

        String fileName = file.getOriginalFilename();
        System.out.println("fileName = " + fileName);
        return new ResponseEntity<>("업로드한 이미지의 이름: " + fileName, HttpStatus.OK);
    }
}
