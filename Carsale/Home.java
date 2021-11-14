package Carsale;

import java.awt.BorderLayout;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;

import java.awt.Font;
import java.awt.Image;

import javax.swing.JTextField;
import javax.imageio.ImageIO;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import javax.swing.JPasswordField;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import java.awt.Color;

public class Home extends JFrame{

	JFrame frame;
	private JTextField textField;
	private JPasswordField passwordField;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Home window = new Home();
					window.frame.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public Home() {
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frame = new JFrame();
		frame.setBounds(100, 100, 675, 493);
		frame.setTitle("WELCOME");
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frame.getContentPane().setLayout(null);
			
		JLabel lblNewLabel = new JLabel("Welcome");
		lblNewLabel.setForeground(new Color(0, 0, 128));
		lblNewLabel.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel.setFont(new Font("Lucida Bright", Font.BOLD, 30));
		lblNewLabel.setBounds(10, 11, 641, 32);
		frame.getContentPane().add(lblNewLabel);
		
		JLabel lblNewLabel_1 = new JLabel("JaviX \r\nCar Sale Management System");
		lblNewLabel_1.setForeground(new Color(160, 82, 45));
		lblNewLabel_1.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel_1.setFont(new Font("Lucida Bright", Font.BOLD, 18));
		lblNewLabel_1.setBounds(10, 53, 641, 42);
		frame.getContentPane().add(lblNewLabel_1);
		
		JLabel lblNewLabel_2 = new JLabel("Username");
		lblNewLabel_2.setForeground(new Color(0, 0, 0));
		lblNewLabel_2.setHorizontalAlignment(SwingConstants.RIGHT);
		lblNewLabel_2.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		lblNewLabel_2.setBounds(48, 134, 196, 32);
		frame.getContentPane().add(lblNewLabel_2);
		
		
		JLabel lblNewLabel_3 = new JLabel("Password");
		lblNewLabel_3.setHorizontalAlignment(SwingConstants.RIGHT);
		lblNewLabel_3.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		lblNewLabel_3.setBounds(48, 196, 196, 30);
		frame.getContentPane().add(lblNewLabel_3);
		
		passwordField = new JPasswordField();
		passwordField.setBounds(278, 199, 205, 32);
		frame.getContentPane().add(passwordField);
		
		
		textField = new JTextField();
		textField.setBounds(278, 136, 205, 32);
		frame.getContentPane().add(textField);
		textField.setColumns(10);
		
		JButton btnNewButton = new JButton("Login");
		btnNewButton.setBackground(new Color(245, 255, 250));
		btnNewButton.setForeground(new Color(0, 0, 128));
		btnNewButton.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				String userName = 	textField.getText();
			    String password = passwordField.getText();
			    if (userName.trim().equals("admin") && password.trim().equals("123")) {
			    	  try
				        {
						 	Admin newWindow = new Admin();
				            newWindow.setVisible(true);
				            textField. setText("");
				            passwordField.setText("");
				            frame.setVisible(false);
				            JOptionPane.showMessageDialog(null, " Login Successful");
				            
				            
				        }
				        catch (Exception ex)
				        {
				            ex.printStackTrace();
				        }
			      } else {
			    	  textField. setText("");
			    	  passwordField.setText(""); 
			    	  JOptionPane.showMessageDialog(null, "Invalid Username or Password. \n               Try again");
			      }
			}
		});
		btnNewButton.setBounds(152, 260, 115, 32);
		frame.getContentPane().add(btnNewButton);
		
		JButton btnNewButton_1 = new JButton("Guest Login");
		btnNewButton_1.setBackground(new Color(245, 255, 250));
		btnNewButton_1.setForeground(new Color(0, 0, 128));
		btnNewButton_1.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				 try
			        {	
					 	Guest newWindow = new Guest();
			            newWindow.setVisible(true);
			            frame.setVisible(false);
			           
			        }
			        catch (Exception ex)
			        {
			            ex.printStackTrace();
			        }
			}
		});
		btnNewButton_1.setBounds(331, 255, 152, 42);
		frame.getContentPane().add(btnNewButton_1);
		
		
		JLabel lblNewLabel_5 = new JLabel("");
		ImageIcon img1 = new ImageIcon(this.getClass().getResource("/resources/img9.png"));
		lblNewLabel_5.setIcon(img1);
		lblNewLabel_5.setBounds(242, 241, 419, 215);
		frame.getContentPane().add(lblNewLabel_5);
		
		JLabel lblNewLabel_4 = new JLabel("");
		ImageIcon img2 = new ImageIcon(this.getClass().getResource("/resources/img14.png"));
		lblNewLabel_4.setIcon(img2);
		lblNewLabel_4.setBounds(-65, 0, 249, 215);
		frame.getContentPane().add(lblNewLabel_4);
		
		
		
		
	}
//	public void setVisible(boolean b) {
//		// TODO Auto-generated method stub
//		
//	}
	
}