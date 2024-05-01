package com.example.demo.Service;
import com.example.demo.Entity.Phishing;
import com.example.demo.Repository.PhishingRepository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class PhishingService {
    private final PhishingRepository phishingRepository;
    private final EntityManager em;

    public int phishingCheck(Phishing phishing){
        int result = 0;
        if(phishing.getIsRedirection()==1) result=1;
        if(phishing.getLongUrl()==1) result=1;
        if(phishing.getHavingIp()==1) result=1;
        if(phishing.getHavingAt()==1) result=1;
        if(phishing.getHavingDash()==1) result=1;
        if(phishing.getHavingUnderbar()==1) result=1;
        if(phishing.getHavingRedirection()==1) result=1;
        if(phishing.getSubDomains()==1) result=1;
        if(phishing.getLongDomain()==1) result=1;
        if(phishing.getSimilarUrl()==1) result=1;
        if(phishing.getNonStandardPort()==1) result=1;
        if(phishing.getIsHttps()==1) result=1;
        if(phishing.getIsTrustedCert()==1) result=1;
        if(phishing.getCreationDate()==1) result=1;
        if(phishing.getExpirationDate()==1) result=1;
        return result;
    }
    public Long create(Phishing phishing){
        phishingRepository.save(phishing);
        return phishing.getId();
    }

    public Phishing findOne(Long id){
        Optional<Phishing> optional_Phishing = phishingRepository.findById(id);
        if(optional_Phishing.isPresent()){
            return optional_Phishing.get();
        }else{
            return null; //추후 변경
        }
    }
}
