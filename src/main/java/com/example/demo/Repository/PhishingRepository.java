package com.example.demo.Repository;
import com.example.demo.Entity.Phishing;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface PhishingRepository extends JpaRepository<Phishing, Long> {
}
