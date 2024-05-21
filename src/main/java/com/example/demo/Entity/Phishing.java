package com.example.demo.Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Data;

import java.util.List;

@Entity @Data
public class Phishing {
    @Id @GeneratedValue
    Long id;

    @Column(name = "is_redirection")
    private Integer isRedirection;

    @Column(name = "long_url")
    private Integer longUrl;

    @Column(name = "having_ip")
    private Integer havingIp;

    @Column(name = "having_at")
    private Integer havingAt;

    @Column(name = "having_dash")
    private Integer havingDash;

    @Column(name = "having_underbar")
    private Integer havingUnderbar;

    @Column(name = "having_redirection")
    private Integer havingRedirection;

    @Column(name = "sub_domains")
    private Integer subDomains;

    @Column(name = "long_domain")
    private Integer longDomain;

    @Column(name = "similar_url")
    private Integer similarUrl;

    @Column(name = "non_standard_port")
    private Integer nonStandardPort;

    @Column(name = "is_trusted_cert")
    private Integer isTrustedCert;

    @Column(name = "is_https")
    private Integer isHttps;

    @Column(name = "get_creation_date")
    private Integer creationDate;

    @Column(name = "get_expiration_date")
    private Integer expirationDate;


    public Phishing(List<Integer> detectedData) {

        this.isRedirection = detectedData.get(0);
        this.longUrl = detectedData.get(1);
        this.havingIp = detectedData.get(2);
        this.havingAt = detectedData.get(3);
        this.havingDash = detectedData.get(4);
        this.havingUnderbar = detectedData.get(5);
        this.havingRedirection = detectedData.get(6);
        this.subDomains = detectedData.get(7);
        this.longDomain = detectedData.get(8);
        this.similarUrl = detectedData.get(9);
        this.nonStandardPort = detectedData.get(10);
        this.isHttps = detectedData.get(11);
        this.isTrustedCert = detectedData.get(12);
        this.creationDate = detectedData.get(13);
        this.expirationDate = detectedData.get(14);

    }

    public Phishing() {

    }
}
