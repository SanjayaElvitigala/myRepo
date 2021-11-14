package Carsale;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.EventQueue;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.SwingConstants;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import java.awt.Font;

import javax.swing.ImageIcon;
import javax.swing.JButton;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class Admin extends JFrame {

	private JPanel contentPane;

	/**
	 * Launch the application.
	 */
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Admin frame1 = new Admin();
					frame1.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the frame.
	 */
	public Admin() {
		setTitle("Admin");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 675, 493);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(null);
		
		JLabel lblNewLabel = new JLabel("Car Sale Management System");
		lblNewLabel.setForeground(new Color(160, 82, 45));
		lblNewLabel.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel.setFont(new Font("Lucida Bright", Font.BOLD, 18));
		lblNewLabel.setBounds(10, 10, 641, 42);
		contentPane.add(lblNewLabel);
		
		JButton btnNewButton = new JButton("Car Details");
		btnNewButton.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		btnNewButton.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Cardetails newWindow1 = new Cardetails();
	            newWindow1.setVisible(true);
	            setVisible(false);
			}
		});
		btnNewButton.setBounds(44, 187, 223, 80);
		contentPane.add(btnNewButton);
		
		JButton btnNewButton_1 = new JButton("Customer Details");
		btnNewButton_1.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		btnNewButton_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				Customerdetails newWindow2 = new Customerdetails();
	            newWindow2.setVisible(true);
	            setVisible(false);
			}
		});
		btnNewButton_1.setBounds(44, 83, 223, 80);
		contentPane.add(btnNewButton_1);
		
		JButton btnNewButton_2 = new JButton("Back");
		btnNewButton_2.setBackground(new Color(245, 255, 250));
		btnNewButton_2.setFont(new Font("Lucida Bright", Font.PLAIN, 18));
		btnNewButton_2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				Home window = new Home();
				window.frame.setVisible(true);
	            setVisible(false);
	            
			}
		});
		btnNewButton_2.setBounds(88, 304, 135, 42);
		contentPane.add(btnNewButton_2);
		
		JLabel lblNewLabel_1 = new JLabel("Admin");
		lblNewLabel_1.setFont(new Font("Lucida Bright", Font.PLAIN, 15));
		lblNewLabel_1.setHorizontalAlignment(SwingConstants.CENTER);
		lblNewLabel_1.setBounds(10, 59, 651, 14);
		contentPane.add(lblNewLabel_1);
		
		JLabel lblNewLabel_3 = new JLabel("");
		ImageIcon img2 = new ImageIcon(this.getClass().getResource("/resources/img12.png"));
		lblNewLabel_3.setIcon(img2);
		lblNewLabel_3.setBounds(130, 138, 565, 308);
		contentPane.add(lblNewLabel_3);
	}
}