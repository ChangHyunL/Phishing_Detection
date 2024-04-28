package socketProgramming;
import Entity.Phishing;
import Service.PhishingService;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;

import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.List;

@RequiredArgsConstructor
public class SocketCommunication {
    private final PhishingService phishingService;
    public static void socketCommunication(String domain){
        try (Socket client = new Socket()) {

            InetSocketAddress ipep = new InetSocketAddress("127.0.0.1", 9999); // 소켓에 접속하기 위한 접속 정보를 선언한다.
            client.connect(ipep);
            try (OutputStream sender = client.getOutputStream(); InputStream receiver = client.getInputStream();) {
                String msg = domain;
                byte[] data = msg.getBytes();
                // ByteBuffer를 통해 데이터 길이를 byte형식으로 변환한다.
                ByteBuffer b = ByteBuffer.allocate(4); //2^32 크기의 데이터 전송
                // byte포멧은 little 엔디언이다.
                b.order(ByteOrder.LITTLE_ENDIAN);
                b.putInt(data.length);
                // 데이터 길이 전송
                sender.write(b.array(), 0, 4);
                sender.write(data);
                //============데이터 전송==============//
                data = new byte[4];
                // 데이터 길이를 받는다.
                receiver.read(data, 0, 4);
                // ByteBuffer를 통해 little 엔디언 형식으로 데이터 길이를 구한다.
                b = ByteBuffer.wrap(data);
                b.order(ByteOrder.LITTLE_ENDIAN);
                int length = b.getInt();
                data = new byte[length];
                receiver.read(data, 0, length);
                msg = new String(data, "UTF-8"); //머신러닝 결과 값
                System.out.println("Socket.msg = " + msg);
                List<Integer> detectedData = splitMsg(msg);//String > List
                System.out.println("detectedData.get(detectedData.size()) = " + detectedData.get(detectedData.size()-1));
                if(detectedData.get(detectedData.size()-1)>0){
                    //phishing domain //phishing=1 //normal=0
                    /*
                    * 피싱 사이트가 탐지되었고 그 결과를 웹으로 전송하려면
                    * 그 결과 값을 파이썬으로부터 받는다는 가정으로 진행 생각
                    * */
                    Phishing newPhishing = new Phishing(detectedData);
                    System.out.println("newPhishing = " + newPhishing);
                }else {
                    //common domain
                    System.out.println("newPhishing = None ");


                }
            }
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }

    private static List<Integer> splitMsg(String msg) {
        // 대괄호와 공백을 제거한 문자열 생성
        String numbersOnly = msg.replaceAll("[\\[\\]\\s]", "");

        // 쉼표를 기준으로 문자열을 분리하여 배열로 변환
        String[] numArray = numbersOnly.split(",");
        // 문자열 배열을 정수 리스트로 변환
        List<Integer> resultList = new ArrayList<>();
        for (String num : numArray) {
            resultList.add(Integer.parseInt(num));
        }
        return resultList;
    }
}
