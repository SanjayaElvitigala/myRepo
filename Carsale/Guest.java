package Carsale;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

import java.awt.Font;
import java.awt.Window;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.awt.event.ActionEvent;
import javax.swing.JTable;
import javax.swing.table.DefaultTableModel;

import net.proteanit.sql.DbUtils;

import javax.swing.JScrollPane;
import javax.swing.SwingConstants;
import javax.swing.JTextField;

public class Guest extends JFrame {
	
	Connection con=null;
	PreparedStatement pst=null;
	ResultSet rs=null;
	
	String url= "jdbc:mysql://localhost/carsale";
	String uname = "root";
	String pass = "";

	private JPanel contentPane;
	private JTable table;
	private JTextField txtCustID;
	private JTextField txtCustName;
	private JTextField txtCustAddress;
	private JTextField txtCustTel;
	private JTextField txtCustDate;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Guest frame = new Guest();
					frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Guest() {
		setTitle("Guest");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 995, 687);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Car Sale management System");
		lblNewLabel.setForeground(new Color(160, 82, 45));
		lblNewLabel.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel.setFont(new Font("Lucida Bright", Font.BOLD, 22));
		lblNewLabel.setBounds(10, 10, 961, 42);
		contentPane.add(lblNewLabel);
		
		JButton btnBuy = new JButton("Buy");
		btnBuy.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnBuy.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
								
				
				buyCar();
			  
	            
			}
		});
		btnBuy.setBounds(848, 498, 125, 39);
		contentPane.add(btnBuy);
		
		JButton btnClose = new JButton("Close");
		btnClose.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnClose.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
	            setVisible(false);
			}
		});
		btnClose.setBounds(846, 597, 125, 39);
		contentPane.add(btnClose);
		
		JScrollPane scrollPane = new JScrollPane();
		scrollPane.setBounds(37, 71, 623, 440);
		contentPane.add(scrollPane);
		
		table = new JTable();
		scrollPane.setViewportView(table);
		table.setModel(new DefaultTableModel(
			new Object[][] {
			},
			new String[] {
				"Model", "Manufacturer", "Year", "Mileage", "Price"
			}
		));
		
		JButton btnShow = new JButton("Show Available Cars");
		btnShow.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				try {
					
					Class.forName("com.mysql.cj.jdbc.Driver");
					con =DriverManager.getConnection(url, uname, pass);
					String query = "SELECT * FROM `cardetails`";
					pst =con.prepareStatement(query);
					rs=pst.executeQuery();
					
					table.setModel(DbUtils.resultSetToTableModel(rs));
					
					
				
				}catch(Exception ex) {
					System.out.println(ex);
				}
				
			}
		});
		btnShow.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnShow.setBounds(37, 549, 182, 38);
		contentPane.add(btnShow);
		
		JLabel lblCustID = new JLabel("ID");
		lblCustID.setHorizontalAlignment(SwingConstants.LEFT);
		lblCustID.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblCustID.setBounds(696, 149, 62, 18);
		contentPane.add(lblCustID);
		
		txtCustID = new JTextField();
		txtCustID.setColumns(10);
		txtCustID.setBounds(792, 146, 164, 28);
		contentPane.add(txtCustID);
		
		JLabel lblCustName = new JLabel("Name");
		lblCustName.setHorizontalAlignment(SwingConstants.LEFT);
		lblCustName.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblCustName.setBounds(696, 183, 62, 29);
		contentPane.add(lblCustName);
		
		txtCustName = new JTextField();
		txtCustName.setColumns(10);
		txtCustName.setBounds(792, 184, 164, 28);
		contentPane.add(txtCustName);
		
		JLabel lblCustAddress = new JLabel("Address");
		lblCustAddress.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblCustAddress.setBounds(696, 232, 75, 18);
		contentPane.add(lblCustAddress);
		
		txtCustAddress = new JTextField();
		txtCustAddress.setColumns(10);
		txtCustAddress.setBounds(792, 229, 164, 28);
		contentPane.add(txtCustAddress);
		
		JLabel lblCustTel = new JLabel("Contact No.");
		lblCustTel.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblCustTel.setBounds(696, 275, 86, 28);
		contentPane.add(lblCustTel);
		
		txtCustTel = new JTextField();
		txtCustTel.setColumns(10);
		txtCustTel.setBounds(792, 277, 164, 28);
		contentPane.add(txtCustTel);
		
		JLabel lblCustDate = new JLabel("Date");
		lblCustDate.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblCustDate.setBounds(696, 322, 62, 27);
		contentPane.add(lblCustDate);
		
		txtCustDate = new JTextField();
		txtCustDate.setColumns(10);
		txtCustDate.setBounds(792, 321, 164, 28);
		contentPane.add(txtCustDate);
		
		JLabel lblNewLabel_2 = new JLabel("Please Fill the below Details ");
		lblNewLabel_2.setForeground(new Color(123, 104, 238));
		lblNewLabel_2.setFont(new Font("Lucida Bright", Font.BOLD, 14));
		lblNewLabel_2.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel_2.setBounds(749, 74, 220, 38);
		contentPane.add(lblNewLabel_2);
		
		JLabel lblNewLabel_3 = new JLabel("Before Buying");
		lblNewLabel_3.setForeground(new Color(112, 128, 144));
		lblNewLabel_3.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel_3.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblNewLabel_3.setBounds(800, 108, 101, 19);
		contentPane.add(lblNewLabel_3);
		
		JLabel lblNewLabel_4 = new JLabel("Select the Car Model");
		lblNewLabel_4.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel_4.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		lblNewLabel_4.setBounds(792, 448, 194, 28);
		contentPane.add(lblNewLabel_4);
		
		JButton btnReg = new JButton("Register");
		btnReg.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				register();
				
			}
		});
		btnReg.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnReg.setBounds(800, 370, 123, 39);
		contentPane.add(btnReg);
		
		JLabel lblNewLabel_1 = new JLabel("");
		lblNewLabel_1.setFont(new Font("Lucida Bright", Font.PLAIN, 13));
		ImageIcon img = new ImageIcon(this.getClass().getResource("/resources/img8.png"));
		lblNewLabel_1.setIcon(img);
		lblNewLabel_1.setBounds(469, 389, 446, 454);
		contentPane.add(lblNewLabel_1);
		
		
		
		JButton btnNewButton_1 = new JButton("Back");
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Home window = new Home();
				window.frame.setVisible(true);
	           
	            setVisible(false);
			}
		});
		btnNewButton_1.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnBuy.setFont(new Font("Lucida Bright", Font.BOLD, 13));
		btnNewButton_1.setBounds(846, 547, 125, 39);
		contentPane.add(btnNewButton_1);
	}
	
	

	public void register() {
		try {
			
			String query = "INSERT INTO `customerreg`(`Id`, `Name`, `Address`, `Contact`, `Date`) VALUES (?,?,?,?,?)";
			Class.forName("com.mysql.cj.jdbc.Driver");
			con =DriverManager.getConnection(url, uname, pass);
			pst =con.prepareStatement(query);
			
			if(txtCustID.getText().length()!=0) {
			pst.setString(1,txtCustID.getText());
			}else
				JOptionPane.showMessageDialog(null,"Enter ID");
			
			if(txtCustName.getText().length()!=0) {	
			pst.setString(2,txtCustName.getText());
			}else
				JOptionPane.showMessageDialog(null,"Enter Name");
			
			if(txtCustAddress.getText().length()!=0) {
			pst.setString(3,txtCustAddress.getText());
			}else
				JOptionPane.showMessageDialog(null,"Enter Address");
			
			if(txtCustTel.getText().length()!=0) {
			pst.setString(4,txtCustTel.getText());
			}else
				JOptionPane.showMessageDialog(null,"Enter Contact Number");
			
			if(txtCustDate.getText().length()!=0) {
			pst.setString(5,txtCustDate.getText());
			}else
				JOptionPane.showMessageDialog(null,"Enter the Date");
			

	
			pst.executeUpdate();
			
	      JOptionPane.showMessageDialog(null,"Successfully Registered");
            }catch(Exception ex) {
//            	JOptionPane.showMessageDialog(null,"Error Occured!"+ex);
            }	
	}
	
	public void buyCar() {
		if(table.getSelectedColumn()==0) {
		int i = table.getSelectedRow();
		String tableVal= table.getValueAt(i, 0).toString();
		JOptionPane.showMessageDialog(null, "You have Successfully bought the car : "+tableVal.toUpperCase());
		}else
			JOptionPane.showMessageDialog(null, "Select Car to Buy");
	}
}
