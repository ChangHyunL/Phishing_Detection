package socketProgramming;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;

public class SocketCommunication {
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

            }
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
}
