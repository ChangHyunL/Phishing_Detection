package Service;

import Entity.Phishing;
import Repository.PhishingRepository;
import jakarta.persistence.EntityManager;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
@RequiredArgsConstructor
public class PhishingService {
    private final PhishingRepository phishingRepository;
    private final EntityManager em;

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
