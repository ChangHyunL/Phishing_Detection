package Entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import lombok.Data;
import org.hibernate.annotations.ValueGenerationType;

@Entity @Data
public class Phishing {
    @Id @GeneratedValue
    Long id;

    @Column(name = "having_IP_Address")
    private Integer havingIPAddress;

    @Column(name = "URL_Length")
    private Integer urlLength;

    @Column(name = "Shortining_Service")
    private Integer shortiningService;

    @Column(name = "having_At_Symbol")
    private Integer havingAtSymbol;

    @Column(name = "double_slash_redirecting")
    private Integer doubleSlashRedirecting;

    @Column(name = "Prefix_Suffix")
    private Integer prefixSuffix;

    @Column(name = "having_Sub_Domain")
    private Integer havingSubDomain;

    @Column(name = "SSLfinal_State")
    private Integer sslFinalState;

    @Column(name = "Domain_registeration_length")
    private Integer domainRegistrationLength;

    @Column(name = "Favicon")
    private Integer favicon;

    @Column(name = "port")
    private Integer port;

    @Column(name = "HTTPS_token")
    private Integer httpsToken;

    @Column(name = "Request_URL")
    private Integer requestURL;

    @Column(name = "URL_of_Anchor")
    private Integer urlOfAnchor;

    @Column(name = "Links_in_tags")
    private Integer linksInTags;

    @Column(name = "SFH")
    private Integer sfh;

    @Column(name = "Submitting_to_email")
    private Integer submittingToEmail;

    @Column(name = "Abnormal_URL")
    private Integer abnormalURL;

    @Column(name = "Redirect")
    private Integer redirect;

    @Column(name = "on_mouseover")
    private Integer onMouseover;

    @Column(name = "RightClick")
    private Integer rightClick;

    @Column(name = "popUpWidnow")
    private Integer popUpWidnow;

    @Column(name = "Iframe")
    private Integer iframe;

    @Column(name = "age_of_domain")
    private Integer ageOfDomain;

    @Column(name = "DNSRecord")
    private Integer dnsRecord;

    @Column(name = "web_traffic")
    private Integer webTraffic;

    @Column(name = "Page_Rank")
    private Integer pageRank;

    @Column(name = "Google_Index")
    private Integer googleIndex;

    @Column(name = "Links_pointing_to_page")
    private Integer linksPointingToPage;

    @Column(name = "Statistical_report")
    private Integer statisticalReport;

    @Column(name = "Result")
    private Integer result;
}
