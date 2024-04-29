package com.example.demo;

import com.example.demo.Entity.Phishing;
import com.google.zxing.*;
import com.google.zxing.client.j2se.BufferedImageLuminanceSource;
import com.google.zxing.common.HybridBinarizer;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import com.example.demo.socketProgramming.SocketCommunication;

import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

@RequiredArgsConstructor
@Component
public class QRcodeScan {
    private static String decodeQRCode(File qrCodeimage) throws IOException {
        BufferedImage bufferedImage = ImageIO.read(qrCodeimage);
        LuminanceSource source = new BufferedImageLuminanceSource(bufferedImage);
        BinaryBitmap bitmap = new BinaryBitmap(new HybridBinarizer(source));

        try {
            Result result = new MultiFormatReader().decode(bitmap);
            return result.getText();
        } catch (NotFoundException e) {
            System.out.println("There is no QR code in the image");
            return null;
        }
    }

    public Phishing scan(String filePath){
        Phishing phishing = null;
        try {
            File file = new File(filePath);
            String decodedText = decodeQRCode(file);
            if(decodedText == null) {
                System.out.println("No QR Code found in the image");
            } else {
                System.out.println("Decoded text = " + decodedText);
            }
            phishing = SocketCommunication.socketCommunication(decodedText);
        } catch (IOException e) {
            System.out.println("Could not decode QR Code, IOException :: " + e.getMessage());
        }
        return phishing;
    }
}
