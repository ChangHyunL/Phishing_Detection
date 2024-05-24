package com.example.demo;

import com.example.demo.Entity.Phishing;
import com.example.demo.Service.PhishingService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.multipart.MultipartFile;
import java.net.HttpURLConnection;
import java.net.URL;

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
    public String handleFileUpload_QRCode(@RequestParam("QRcodeImage") MultipartFile file, Model model) throws IOException {
        int phishingCheck=0;
        System.out.println("file = " + file);
        System.out.println("file.isEmpty() = " + file.isEmpty());
        if (file.isEmpty()) {
            return "redirect:scan";
        }

        String fileName = file.getOriginalFilename();
        System.out.println("fileName = " + fileName);
        String UPLOAD_DIR  = "C:\\Users\\Administrator\\Pictures\\QRcodes\\"; //저장할 디렉토리 이름
        String filePath = UPLOAD_DIR + fileName;
        File dest = new File(filePath);
        file.transferTo(dest);
        Phishing result = qrCodeScan.scan(filePath);
        File file1 = new File(filePath);
        String originalURL = QRcodeScan.decodeQRCode(file1);
        String redirectURL = null;
        try {
            URL url = new URL(originalURL);
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setInstanceFollowRedirects(false); // 리다이렉션을 따르지 않도록 설정
            int responseCode = connection.getResponseCode();

            if (responseCode >= 300 && responseCode < 400) { // 리다이렉션 상태 코드인 경우
                redirectURL = connection.getHeaderField("Location");
                System.out.println("Redirect URL: " + redirectURL);
            } else {
                System.out.println("No redirection.");
            }

            connection.disconnect();
        } catch (IOException e) {
            model.addAttribute("wrongUrl", 1);
            e.printStackTrace();
        }

        phishingCheck = phishingService.phishingCheck(result);
        if(phishingCheck==1){
            phishingService.create(result);
            model.addAttribute("phishingCheck", phishingCheck);
        }
        model.addAttribute("url", redirectURL);
        model.addAttribute("result",result);
        model.addAttribute("wrongUrl", 0);
        System.out.println("handleFileUpload_QRCode_result = " + result);
        return "QRcodeScanner";
    }
    @PostMapping("/scanURL")
    public String handleFileUpload_URL(@RequestParam("url") String url, Model model){
        int phishingCheck=0;
        if (url.isEmpty()) {
            return "redirect:scan";
        }
        try {
            System.out.println("url = " + url);
            URL urlObj = new URL(url);
            HttpURLConnection connection = (HttpURLConnection) urlObj.openConnection();
            connection.setRequestMethod("HEAD");
            int responseCode = connection.getResponseCode();
            System.out.println("connection.getURL() = " + connection.getURL());
            System.out.println("Response Code: " + responseCode);

            connection.disconnect();

        }catch ( Exception e) {
            e.printStackTrace();
            //URL이 아닌 값
            model.addAttribute("wrongUrl", 1);
            return "QRcodeScanner";
        }

        Phishing result = urlScan.scan(url); //정상 URL > 모두 0, 피싱 URL > '1' 포함
        phishingCheck = phishingService.phishingCheck(result);
        if(phishingCheck==1){
            phishingService.create(result);
            System.out.println("handleFileUpload_URL_result = " + result);
            model.addAttribute("phishingCheck", phishingCheck);
        }
        model.addAttribute("url", url);
        model.addAttribute("result",result);
        model.addAttribute("wrongUrl", 0);

        return "QRcodeScanner";
    }
}
