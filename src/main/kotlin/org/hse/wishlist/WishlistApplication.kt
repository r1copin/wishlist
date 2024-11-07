package org.hse.wishlist

import org.springframework.boot.autoconfigure.SpringBootApplication
import org.springframework.boot.runApplication
import java.lang.Thread.sleep

@SpringBootApplication
class WishlistApplication

fun main(args: Array<String>) {
	while (true) {
		sleep(10_000)
		println("Slept")
	}
	//runApplication<WishlistApplication>(*args)
}
