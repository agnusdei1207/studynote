// ========================================
// Chapter 01: Hello Rust & Cargo 기초
// ========================================

// 이것은 주석입니다. 컴파일러가 무시합니다.
// Rust에서 주석은 // 로 시작합니다.

/*
 이것은 여러 줄 주석입니다.
 여러 줄에 걸쳐 설명을 작성할 수 있습니다.
*/

/// 이것은 문서화 주석입니다.
/// cargo doc 명령으로 HTML 문서를 생성할 수 있습니다.

// main 함수: 프로그램의 시작점
fn main() {
    // 1. 기본 출력
    println!("Hello, world!");
    
    // 2. 여러 줄 출력
    println!("안녕하세요!");
    println!("Rust 학습을 시작합니다!");
    
    // 3. 빈 줄 출력
    println!();
    
    // 4. 변수 사용하기 (미리보기)
    let name = "Rustacean";  // 불변 변수 선언
    println!("저는 {}입니다.", name);
    
    // 5. 여러 값 출력하기
    let language = "Rust";
    let year = 2026;
    println!("{}년, {} 학습 시작!", year, language);
    
    // 6. 디버그 출력 ({:?})
    println!("디버그 출력: {:?}", (name, language, year));
}
