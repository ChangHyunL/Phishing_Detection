package com.example.demo;
import com.example.demo.Entity.Phishing;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Component;
import com.example.demo.socketProgramming.SocketCommunication;

@RequiredArgsConstructor
@Component
public class UrlScan {
    public Phishing scan(String url){
        Phishing phishing = SocketCommunication.socketCommunication(url);
        return phishing;
    }
}
