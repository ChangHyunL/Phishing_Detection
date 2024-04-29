package com.example.demo;

import com.example.demo.Entity.Phishing;
import com.example.demo.Service.PhishingService;
import lombok.RequiredArgsConstructor;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;
import java.io.IOException;

@Controller
@RequiredArgsConstructor
public class MainController {
    private final QRcodeScan qrCodeScan;
    private final UrlScan urlScan;
    private final PhishingService phishingService;
    @GetMapping("/scan")
    public String scan(){
        return "QRcodeScanner";
    }

    @PostMapping("/scanQRcode")
    public String handleFileUpload_QRCode(@RequestParam("image") MultipartFile file) throws IOException {
        if (file.isEmpty()) {
            return null;
        }

        String fileName = file.getOriginalFilename();
        System.out.println("fileName = " + fileName);
        String UPLOAD_DIR  = "C:\\Users\\Public\\Python_tool\\QR_Codes\\"; //저장할 디렉토리 이름
        String filePath = UPLOAD_DIR + fileName;
        File dest = new File(filePath);
        file.transferTo(dest);

        Phishing result = qrCodeScan.scan(filePath);

        System.out.println("handleFileUpload_QRCode_result = " + result);
        return "QRcodeScanner";
    }
    @PostMapping("/scanURL")
    public String handleFileUpload_URL(@RequestParam("url") String url, Model model){
        if (url.isEmpty()) {
            return null;
        }

        Phishing result = urlScan.scan(url);
        phishingService.create(result);
        System.out.println("handleFileUpload_URL_result = " + result);
        model.addAttribute("result", url);
        return "QRcodeScanner";
    }
}
