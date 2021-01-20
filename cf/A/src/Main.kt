import java.util.ArrayList
import java.util.Collections
import java.util.Scanner

object Main {

    internal class Pair(var first: Int, var second: Int) : Comparable<Pair> {

        override fun compareTo(other: Pair): Int {
            return if (this.first < other.first) {
                -1
            } else if (this.first > other.first) {
                1
            } else {
                if (this.second < other.second) {
                    -1
                } else if (this.second > other.second) {
                    1
                } else {
                    0
                }
            }
        }

        override fun hashCode(): Int {
            val prime = 17
            var result = 1
            result = prime * result + first
            result = prime * result + second
            return result
        }


        override fun equals(other: Any?): Boolean {
            return if (other is Pair) {
                other.first == this.first && other.second == this.second
            } else false
        }
    }

    @JvmStatic
    fun main(args: Array<String>) {
        val `in` = Scanner(System.`in`)
        val N = `in`.nextInt()
        val M = `in`.nextInt()
        for (i in 0 until M){
            break
        }
        val K = `in`.nextInt()
        val matrix = ArrayList<Pair>()
        for (i in 0 until N) {
            matrix.add(Pair(`in`.nextInt(), i + 1))
        }
        Collections.sort(matrix)
        val ans = ArrayList<ArrayList<Int>>()
        for (i in 0 until K) {
            ans.add(ArrayList())
        }
        for (i in 0 until N) {
            ans[i % K].add(matrix[i].second)
        }
        for (i in 0 until K) {
            print(ans[i].size)
            print(" ")
            for (j in 0 until ans[i].size) {
                print(ans[i][j])
                print(" ")
            }
            println()
        }
    }
}
